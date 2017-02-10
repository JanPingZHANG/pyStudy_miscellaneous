import asyncio

async def abc():
	a=0
	for i in range(100):
		a = a+i
	print('from async method a: ',a)
	return a

def asAbc():
	a = 0
	return a

async def test():
	#a = await asAbc()
	print('start test')
	#print('a: ',a)
	print('await a async method')
	a = await abc()
		print('a: ',a)
	print('end test')

if __name__ == '__main__':
	print(type(test))
	print(type(abc))
	loop = asyncio.get_event_loop()
	loop.run_until_complete(test())
	loop.close()
