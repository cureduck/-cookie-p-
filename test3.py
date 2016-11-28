from chormecookiejar import MyCookieJar
from urllib import request
import urllib
from aiohttp.web import Response
import logger


cookieJ=MyCookieJar()
cookieJ.load()
handler=request.HTTPCookieProcessor(cookieJ)
opener=request.build_opener(handler)

response=opener.open('http://www.pixiv.net/')
cookieJ.save()
print(response)
data=response.read()

logger.logger(data)
