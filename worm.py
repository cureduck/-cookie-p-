from urllib import request
from bs4 import BeautifulSoup
import sys
import gzip
import time
import os


def get_content(url,headers):
    req=request.Request(url)
    req.headers=headers
    with request.urlopen(req) as f:
        Content_Type=f.headers.get('Content-Type')
        Content_Encoding=f.headers.get('Content-Encoding')
        data=f.read()
        if Content_Encoding:
            data=gzip.decompress(data)
        data=data.decode('UTF-8')

        return data


def download(url,headers,path,name):
    req=request.Request(url)
    req.headers=headers
    with request.urlopen(req) as f:
        file=open(path+'/'+name+'.jpg','wb')
        data=f.read(1024)
        while data!=b'':
            file.write(data)
            data=f.read(1024)
        file.close()

def create_dic(path):
    now_time = str(int(time.time()))
    today_pics = path+'/pixiv每日图片/' + now_time
    if os.path.exists(today_pics):
        pass
    else:
        os.makedirs(today_pics)
    return today_pics

#----------------------------------------------------找pixiv每日图片所在的网页--------------------------------------------------------------


headers_htai = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Cookie': '_ga=GA1.2.1471600395.1476429356; _gat=1',
        'Host': 'htai.co',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}



data=get_content('http://htai.co/pixiv',headers_htai)

#-------------------------------------------------------将网页中的有用信息提取出来----------------------------------------------------------------------------------------------
bs=BeautifulSoup(data,"html.parser")

pic_url=[]                                  #url的list，装(img,herf)的tuple
aimDivs=bs.find_all(name='div',attrs='cell') #aimDiv是resultSet类型，是list子类（大概？）
for aimDiv in aimDivs:                             #aimDiv是个tag类，可以用dir(aimDiv)查看他的方法
    aimHerf=aimDiv.findChild(name='a').get('href').replace('medium','manga')
    #aimHerf=aimHerf.split('?')[-1]
    pic_url.append(aimHerf)


headers_pixiv={
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate, sdch',
    'Accept-Language':'zh-CN,zh;q=0.8',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'p_ab_id=0; login_ever=yes; a_type=0; is_sensei_service_user=1; module_orders_mypage=%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; _ga=GA1.2.383889308.1478570004; ki_t=1478570308868%3B1479878016466%3B1479889682790%3B4%3B12; ki_r=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DWuBwAE5zrV27k38aYNlPpEW2XQMy2NJwCOK1nKancVO%26wd%3D%26eqid%3D88f24c850000286300000005583552d8; PHPSESSID=509bba24b654a4e05d5ec9735bb465d2; __utmt=1; __utma=235335808.383889308.1478570004.1479887981.1479894803.10; __utmb=235335808.2.10.1479894803; __utmc=235335808; __utmz=235335808.1479790613.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=20981040=1',
    'Host':'www.pixiv.net',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
}

path=create_dic('D:')
count=0
for herf in pic_url:
    print(herf)
    data=get_content(herf,headers_pixiv)


    bs=BeautifulSoup(data,'html.parser')
    Img_urls=bs.find_all(name='img',attrs={'class':'ui-scroll-view'})



    headers_single_pic = {
        'Accept': 'image/webp,image/*,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        #'Cookie': 'p_ab_id=0; module_orders_mypage=%5B%7B%22name%22%3A%22spotlight%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22everyone_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22sensei_courses%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22hot_entries%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22featured_tags%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22contests%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22following_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22mypixiv_new_illusts%22%2C%22visible%22%3Atrue%7D%2C%7B%22name%22%3A%22booth_follow_items%22%2C%22visible%22%3Atrue%7D%5D; _ga=GA1.2.383889308.1478570004; PHPSESSID=509bba24b654a4e05d5ec9735bb465d2; __utmt=1; __utma=235335808.383889308.1478570004.1479887981.1479894803.10; __utmb=235335808.5.10.1479894803; __utmc=235335808; __utmz=235335808.1479790613.5.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=235335808.|2=login%20ever=yes=1^3=plan=normal=1^5=gender=male=1^6=user_id=20981040=1',
        'Host': 'i4.pixiv.net',
        'Referer': herf,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    }

    for img in Img_urls:
        pic_url=img.get('data-src')
        count=count+1
        download(pic_url,headers_single_pic,path,str(count))

print(pic_url)


# --------------------------------------------------建立文件夹---------------------------------------------------------------------------------------------



#-------------------------------------------------前往pixiv -----------------------------------------------------------------------






""""

i=0
for item in pic_url:
    i=i+1
    img=item[0]
    herf=item[1]
    f=open(today_pics+'/'+herf+'.jpg','wb')
    content=request.urlopen(img).read()
    f.write(content)
    f.close()
"""
