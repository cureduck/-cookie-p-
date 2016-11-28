from urllib import request
from bs4 import BeautifulSoup
import gzip
import time
import os


def get_content(url, headers, cookiejar=None, content=None):
    handler = request.HTTPCookieProcessor(cookiejar)
    opener = request.build_opener(handler)
    opener.headers = headers
    try:
        with opener.open(fullurl=url, data=content) as response:
            content_type=response.headers.get('Content-Type')
            content_encoding=response.headers.get('Content-Encoding')
            data=response.read()
            if content_encoding:
                data=gzip.decompress(data)
            data=data.decode('UTF-8')
            return data

    except BaseException as e:
        print(e,':',url)

