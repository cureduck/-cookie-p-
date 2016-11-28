from http.cookiejar import Cookie,iso2time,CookieJar,_threading,DefaultCookiePolicy
import os
import sys
import sqlite3
from crypt import decrypt,encrypt
import time




#参考http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-queryd的做法，用它重载cursor的row_factory可以返回dict（原本是tuple）
def dict_factory(cursor,row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


#用来将一个{key:value}的dict来构建cookie实例
def make_cookie(cookie_dict):
    h = cookie_dict.get
    expires = h('expires_utc')
    discard = h('discard',False)
    domain = h('host_key')
    value=h('value')
    initial_dot = domain.startswith('.')
    domain_specified=initial_dot
    if expires is not None:
        expires = int(expires/1000000)-11644473600
    else:
        discard = True
    if value is None or value == '':
        pwdhash = h('encrypted_value')
        try:
            value = decrypt(pwdhash).decode()
        except:
            pass

    return Cookie(
        version=h('version', 0),
        domain=domain, domain_specified=domain_specified, domain_initial_dot=initial_dot,
        path=h('path'), path_specified=h('path_spec', True),
        name=h('name'),
        value=value,
        port=h('port'), port_specified=h('port_spec', False),
        expires=expires, discard=discard,
        secure=bool(h('secure')),
        comment=h('comment'), comment_url=h('comment_url'),
        rest={}
    )

class MyCookieJar(CookieJar) :
#大部分是参照CookieJar的实现来做的，多建立了两个变量
    def __init__(self, policy=None):
        if policy is None:
            policy = DefaultCookiePolicy()
        self._policy = policy
        self._policy._now = self._now = int(time.time())
        self._cookies_lock = _threading.RLock()
        self._cookies = {}
        self._new_cookies=[]                    #由于cookies要存到数据库，所以需要记录哪些cookie是新添加的，哪些cookie是被更新了
        self._renewed_cookies=[]

        if sys.platform == 'win32':             #平台判断，不同的平台cookie存放的位置不同
            self.cookie_path = os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/cookies'
        elif sys.platform == 'darwin':
            self.cookie_path = 'Users/' + os.environ['USER'] + '/Library/Application Support/Google/Chrome/Default/Cookies'
        else:
            raise BaseException('Unknown Platform')

#获取本地chrome保存的cookie
    def get_chrome_cookie(self):
        with sqlite3.connect(self.cookie_path) as conn:
            cur = conn.cursor()
            cur.row_factory = dict_factory          #重载row_factory
            sql = 'select * from cookies'
            result = cur.execute(sql).fetchall()
            for cookie_dict in result:
                self.set_cookie(make_cookie(cookie_dict))

    def load(self):
        self.get_chrome_cookie()

#将有新添加的cookies保存到内存中，在save的时候再将它们添加的数据库中
    def save_changed_cookie(self, cookie):
        c = self._cookies
        self._cookies_lock.acquire()
        try:
            if c.get(cookie.domain, None)is None:
                self._new_cookies.append(cookie)
                return
            c2 = c[cookie.domain]
            if c2.get(cookie.path, None)is None:
                self._new_cookies.append(cookie)
                return
            c3 = c2[cookie.path]
            if c3.get(cookie.name, None)is None:
                self._new_cookies.append(cookie)
                return
            self._renewed_cookies.append(cookie)
        finally:
            self._cookies_lock.release()

#extract_cookies是用来从response中把cookie有关的内容剥离出来并将其保存到self._cookies的，由于我要实现的目的需要把只把新添加的cookies
#保存到数据库中（在ookieJarC类的原本做法中是每一次save都把cookie文件删了重来，毕竟它保存的cookie性质上是临时文件，而我在操作的是chrome
#的cookies数据库，每次都重来不仅费时，还很危险 ），所以在处理逻辑上有所改变，这比较复杂，如果你有兴趣可以私聊我
    def extract_cookies(self, response, request):
        """Extract cookies from response, where allowable given the request."""
        self._cookies_lock.acquire()
        try:
            for cookie in self.make_cookies(response, request):
                if self._policy.set_ok(cookie, request):
                    self.save_changed_cookie(cookie)
                    self.set_cookie(cookie)
        finally:
            self._cookies_lock.release()

#这是将cookies insert 或者update到数据库中的方法，cookie中的数据项与chrome数据库中的数据项之间的映射关系也搞了我好久，如果你有兴趣，私聊我
    def save(self):
        with sqlite3.connect(self.cookie_path) as conn:
            cur=conn.cursor()
            sql_insert = 'insert into cookies (host_key,name,path,expires_utc,encrypted_value,creation_utc,last_access_utc,secure,value,httponly) values(?,?,?,?,?,?,?,?,'',0)'
            sql_update = 'update cookies set expires_utc=?,encrypted_value=?,last_access_utc=? where host_key=? and name=? and path=?'
            for cookie in self._new_cookies:
                if cookie.expires and cookie.expires<time.time():
                    para = (cookie.domain,cookie.name, cookie.path,
                            (cookie.expires+11644473600)*1000000, encrypt(bytes(cookie.value,encoding='utf-8')),
                            int((time.time()+11644473600)*1000000), int((time.time()+11644473600)*1000000),
                            int(cookie.secure),'',cookie._rest.get('httponly',0))
                    print(sql_insert,para)
                    cur.execute(sql_insert, para)
            for cookie in self._renewed_cookies:
                para = (cookie.expires, encrypt(bytes(cookie.value, encoding='utf-8')),
                        int((time.time()+11644473600)*1000000), cookie.domain, cookie.name, cookie.path)
                cur.execute(sql_update, para)




