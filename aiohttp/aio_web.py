from aiohttp import web
import asyncio

async def index(request):
	f = open('test.csv','rb')
	data = f.read()
	f.close()
	return web.Response(body=data,content_type='file')

async def get_csv1(resuest):
	f = open('test1.csv','rb')
	data = f.read()
	f.close()
	return web.Response(body=data,content_type='file')

async def init(loop):
	app = web.Application(loop=loop)
	app.router.add_route('GET','/',index)
	app.router.add_route('GET',r'/csv/1',get_csv)
	srv = await loop.create_server(app.make_handler(),'127.0.0.1',8000)
	print('server started at 127.0.0.1:8000...')
	#print(callable(srv))
	return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
