import asyncio

global __pool
__pool=1

@asyncio.coroutine
def lo():
	global __pool
	__pool = 1

@asyncio.coroutine
def printResult():
	global __pool
	yield from __pool
	print(__pool)

print('start')
lo()
loop = asyncio.get_event_loop()                                             
loop.run_until_complete(printResult())
loop.close()
print('end')

