import asyncio

def put(n):
	print(n)

def loop1():
	for i in range(5):
		print('loop1 %d'%i)
		yield put(i)

def loop2():
	for i in range(5):
		print('loop2 %d'%i)
		yield put(i)

@asyncio.coroutine
def main():
	a = yield from loop1()
	print(a)
	b = yield from loop2()
	print(b)

if __name__=='__main__':
	loop = asyncio.get_event_loop()
	loop.run_until_complete(main())
