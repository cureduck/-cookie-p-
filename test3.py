from chormecookiejar import MyCookieJar
from urllib import request
import logger
import gzip
from bs4 import BeautifulSoup
import time
import os

def get_content(url, opener, headers, content=None):
    req = request.Request(url)
    req.headers=headers
    try:
        with opener.open(req) as f:
            content_type=f.headers.get('Content-Type')
            content_encoding=f.headers.get('Content-Encoding')
            data=f.read()
            if content_encoding :
                data=gzip.decompress(data)
            data=data.decode('UTF-8')
            return data
    except BaseException as e:
        print(e, ':', url)


def download(url, opener, headers, name, path='D:/pixiv每日图片'):
    req = request.Request(url)
    req.headers = headers
    try:
        with opener.open(req) as f:
            with open(path+'/'+name+'.jpg', 'wb') as file:
                data=f.read(1024)
                while data != b'':
                    file.write(data)
                    data = f.read(1024)

    except BaseException as e:
        print(e, ':', url)


headers_htai = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}


headers_pixiv={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

headers_pixiv_pic = {
    'Accept': 'image/webp,image/*,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Referer': ''
}


cookieJ = MyCookieJar()
cookieJ.load()
handler = request.HTTPCookieProcessor(cookieJ)
opener = request.build_opener(handler)

htai_content = get_content('http://htai.co/pixiv', opener, headers_htai)
bs = BeautifulSoup(htai_content, 'html.parser')
pic_url = []
aimDivs = bs.find_all(name='div', attrs='cell')
for aimDiv in aimDivs:
    aimHref = aimDiv.findChild(name='a').get('href')
    pic_url.append(aimHref)


save_path = 'D:/pixiv每日图片/'+str(time.strftime('%Y-%m-%d', time.localtime()))
if not os.path.exists(save_path):
    os.makedirs(save_path)
count=0
for href in pic_url:
    print(href)
    pixiv_html = get_content(href, opener, headers_pixiv)
    bs = BeautifulSoup(pixiv_html, 'html.parser')
    img_sources = bs.find_all(name='img', attrs={'class': 'original-image'})
    for img_source in img_sources:
        count += 1
        img_url = img_source.get('data-src')
        headers_pixiv_pic['Referer']=href
        download(img_url, opener, headers_pixiv_pic,str(count),save_path)

cookieJ.save()