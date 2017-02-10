import asyncio
import logging;logging.basicConfig(level=logging.INFO)
import aiomysql

@asyncio.coroutine
def createPool(loop,**kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = yield from aiomysql.create_pool(
	host = kw.get('host','localhost'),
	port = kw.get('port',3306),
	user = kw['user'],
	password = kw['password'],
	db = kw['db'],
	charset = kw.get['charset','utf-8'],
	autocommit = kw.get['autocommit',True],
	maxsize = kw.get['maxsize',10],
	minsize = kw.get['minsize',1],
	loop = loop,
	)

@asyncio.coroutine
def select(sql,args,size=None):
	global __pool
	with (yield from __pool) as conn:
		cur = yield from conn.cursor(aiomysql.DictCursor)
		yield from cur.execute(sql.replace('?','%s'),args or ())
		if size:
			rs = yield from cur.fetchmany(size)
		else:
			rs = yield from cur.fetchall()
		yield from cur.close()
		logging.info('rows returned %s'%len(rs))
		return rs

@asyncio.coroutine
def execute(sql,args):
	with(yield from __pool) as conn:
		try:
			cur = yield from conn.cursor()
			yield from cur.execute(sql.replace('?','%s'),args)
			affected = cur.rowcount
			yield from cur.close()
		except BadException as e:
			raise
		return affected
			

	
if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	global __pool
	#loop.run_until_complete(createPool(loop,user='root',db='test',password='z5827468'))
	print(__pool)
