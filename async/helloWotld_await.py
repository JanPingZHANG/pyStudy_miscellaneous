import asyncio
from time import sleep,ctime

async def hello():
	print ('hello world')
	r=await asyncio.sleep(1)
	print ('hello again')

tasks=[hello(),hello()]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop.close()
