import aiomysql
import asyncio

async def createPool(loop,**kw):
	global __pool
	__pool = await aiomysql.create_pool(
	host = 'localhost',
	port = 3306,
	user = 'www-data',
	password = 'www-data',
	db = 'awesome',
	charset = 'utf8',
	autocommit = True,
	maxsize = 10,
	minsize =1,
	loop = loop
	)

async def insertUser(id,email,passwd,admin,name,image,created_at):
	values = str(id)+',"'+str(email)+'","'+str(passwd)+'",'+str(admin)+',"'+str(name)+'","'+str(image)+'","'+str(created_at)+'"'
	sql = 'insert into users(id,email,passwd,admin,name,image,created_at) values(%s)'%values
	global __pool
	async with __pool.get() as conn:
		try:
			async with conn.cursor() as cur:
				await cur.execute(sql)
				affected = cur.rowcount
		except BaseException as e:
			raise(e,'\n SQL: ',sql)
	return affected

loop = asyncio.get_event_loop()
loop.run_until_complete(createPool(loop))
#loop.run_until_complete(insertUser(125,'999@123.com','123456',1,'david','image',5657678))
loop.close()
#print(asyncio.iscoroutine(__pool.get))
await __pool
