import logging; logging.basicConfig(level=logging.INFO)
from logger import logger
import asyncio
from aiohttp import web



"""
这是一个只接收request并将request打印出来的模拟器，在127.0.0.1：9000，只接受http协议get方法
只要点那个运行就可以了
"""
async def index(request):
    headers=dict(**request.headers)                                         #很多类dict而不是dict的子类的类都可以用dict(a)方法或者dict(**a)来使其变成dict类
    cookie=headers.get('Cookie')
    if cookie:logger(cookie)
    for k,v in headers.items():
        print(k,':',v)

    kw = dict(**(await request.post()))
    for k,v in kw.items():
        print(k,':',v)

    print('--------------------------------------------------------')



    return web.Response(body=b'<h1>Awesome</h1>')


async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()