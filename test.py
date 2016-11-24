from http import cookiejar
from urllib import request
import gzip




def get_content(url,headers):
    req = request.Request(url)
    req.headers = headers
    cookie = cookiejar.CookieJar()
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    try:
        for item in cookie:
            print('name:',item.name)
            print('value:',item.value)
        with opener.open(req) as f:
            content_type=f.headers.get('Content-Type')
            content_encoding=f.headers.get('Content-Encoding')
            data=f.read()
            if content_encoding:
                data = gzip.decompress(data)
            data = data.decode('UTF-8')

            return data
    except BaseException as e:
        print(e,':',url)

headers={
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/54.0.2840.99 Safari/537.36',
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #'Referer':'http://www.pixiv.net/member_illust.php?mode=medium&illust_id=60052998&uarea=daily',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8'
    #'Cookie':'p_ab_id=0; login_ever=yes; module_orders_mypage=%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; PHPSESSID=20981040_e5430321213a59e745c91c0efd73a56c; __utma=235335808.383889308.1478570004.1479887981.1479894803.10; __utmb=235335808.4.10.1479894803; __utmz=235335808.1479790613.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=20981040=1; _ga=GA1.2.383889308.1478570004'
}

data=get_content('http://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001432688314740a0aed473a39f47b09c8c7274c9ab6aee000',headers)
data=get_content('http://baidu.com',headers)