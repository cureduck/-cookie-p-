from http.cookiejar import Cookie,iso2time,CookieJar,_threading,DefaultCookiePolicy
import os
import sys
import sqlite3
from crypt import decrypt,encrypt
import time




#参考http://stackoverflow.com/questions/3300464/how-can-i-get-dict-from-sqlite-queryd的做法，返回dict
def dict_factory(cursor,row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
#-----------------------------------------------------------------------------------------------------

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




class MyCookieJar(CookieJar):

    def __init__(self, policy=None):
        if policy is None:
            policy = DefaultCookiePolicy()
        self._policy = policy
        self._policy._now = self._now = int(time.time())
        self._cookies_lock = _threading.RLock()
        self._cookies = {}
        self._new_cookies=[]
        self._renewed_cookies=[]

        if sys.platform == 'win32':
            self.cookie_path = os.environ['LOCALAPPDATA'] + '/Google/Chrome/User Data/Default/cookies'
        elif sys.platform == 'darwin':
            self.cookie_path = 'Users/' + os.environ['USER'] + '/Library/Application Support/Google/Chrome/Default/Cookies'
        else:
            raise BaseException('Unknown Platform')

    def get_chrome_cookie(self):
        with sqlite3.connect(self.cookie_path) as conn:
            cur = conn.cursor()
            cur.row_factory = dict_factory
            sql = 'select * from cookies'
            result = cur.execute(sql).fetchall()
            for cookie_dict in result:
                self.set_cookie(make_cookie(cookie_dict))

    def load(self):
        self.get_chrome_cookie()

    def save_changed_cookie(self, cookie):
        c = self._cookies
        self._cookies_lock.acquire()
        try:
            if cookie.domain not in c[cookie.domain]:
                self._new_cookies.append(cookie)
                return
            c2 = c[cookie.domain]
            if cookie.path not in c2[cookie.path]:
                self._new_cookies.append(cookie)
                return
            c3 = c2[cookie.path]
            if cookie.name not in c3[cookie.name]:
                self._new_cookies.append(cookie)
                return
            self._renewed_cookies.append(cookie)
        finally:
            self._cookies_lock.release()

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

    def save(self):
        with sqlite3.connect(self.cookie_path) as conn:
            cur=conn.cursor()
            sql_insert = 'insert into cookies (host_key,name,path,expires_utc,encrypted_value,creation_utc,last_access_utc,secure,value,httponly) values(?,?,?,?,?,?,?,?,'',0)'
            sql_update = 'update cookies set expires_utc=?,encrypted_value=?,last_access_utc=? where host_key=? and name=? and path=?'
            for cookie in self._new_cookies:
                para = (cookie.domain,cookie.name, cookie.path, (cookie.expires+11644473600)*1000000, encrypt(bytes(cookie.value,encoding='utf-8')), int(time.time()), int(time.time()), cookie.secure)
                cur.execute(sql_insert, para)
            for cookie in self._renewed_cookies:
                para = (cookie.expires, encrypt(bytes(cookie.value, encoding='utf-8')), int(time.time()), cookie.domain, cookie.name, cookie.path)
                cur.execute(sql_update, para)



cookieJ = MyCookieJar()
cookieJ.load()
print('good')
