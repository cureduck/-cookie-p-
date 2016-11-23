from urllib import request
from bs4 import BeautifulSoup
import sys
import gzip
import time
import os

#----------------------------------------------------找pixiv每日图片所在的网页--------------------------------------------------------------
url='http://htai.co/pixiv'

req = request.Request(url)
req.add_header('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
req.add_header('Accept-Encoding','gzip, deflate, sdch')
req.add_header('Accept-Language','zh-CN,zh;q=0.8')
req.add_header('Cache-Control','max-age=0')
req.add_header('Connection','keep-alive')
req.add_header('Cookie','BAIDU_SSP_lcr=https://www.baidu.com/link?url=9GCf5NWMM252Sfwiz-JPjm586uqdGAOZexokxYjDj2e&wd=&eqid=84abf69100011bab000000055835312d; _gat=1; _ga=GA1.2.1471600395.1476429356')
req.add_header('Host','htai.co')
req.add_header('Referer','http://www.htai.co/')
req.add_header('Upgrade-Insecure-Requests','1')
req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')
with request.urlopen(req) as f:
    print('Status:', f.status, f.reason)
    for k,v in f.getheaders():
        print(k,':',v)

    data=f.read().decode('utf-8')

#-------------------------------------------------------将网页中的有用信息提取出来----------------------------------------------------------------------------------------------
bs=BeautifulSoup(data,"html.parser")

pic_url=[]                                  #url的list，装(img,herf)的tuple
aimDivs=bs.find_all(name='div',attrs='cell') #aimDiv是resultSet类型，是list子类（大概？）
for aimDiv in aimDivs:                             #item是个tag类，可以用dir(item)查看他的方法
    aimImg=aimDiv.findChild(name='img').get('src')
    aimHerf=aimDiv.findChild(name='a').get('href')
    #aimHerf=aimHerf.split('?')[-1]
    pic_url.append((aimImg,aimHerf))

print(pic_url)

#--------------------------------------------------建立文件夹---------------------------------------------------------------------------------------------

now_time=str(int(time.time()))
today_pics='D:/pixiv每日图片/'+now_time
if os.path.exists(today_pics):
    pass
else:
    os.makedirs(today_pics)

#-------------------------------------------------下载图片-----------------------------------------------------------------------


i=0
for item in pic_url:
    i=i+1
    img=item[0]
    herf=item[1]
    f=open(today_pics+'/'+herf+'.jpg','wb')
    content=request.urlopen(img).read()
    f.write(content)
    f.close()

