from http.cookiejar import MozillaCookieJar
from urllib import request
import urllib
from aiohttp.web import Response

cookieJ=MozillaCookieJar('D:/cookies')
handler=request.HTTPCookieProcessor(cookieJ)
opener=request.build_opener(handler)

response=opener.open('http://www.baidu.com')
cookieJ.save()
print(response)
print(response.read())
