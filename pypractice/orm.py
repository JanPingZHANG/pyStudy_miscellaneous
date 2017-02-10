import asyncio
import logging;logging.basicConfig(level=logging.INFO)
import aiomysql

def log(sql,args=()):
	logging.info('SQL: %s' % sql)

def listToStr(ls):
	s=''
	count = len(ls)
	for i in range(count):
		if i==count-1:
			s = s + ls[i]
		else :
			s = s + ls[i] + ','
	return s

async def create_pool(loop,**kw):
	logging.info('create database connection pool...')
	global __pool
	__pool = await aiomysql.create_pool(
	host = kw.get('host','localhost'),
	port = kw.get('port',3306),
	user = kw['user'],
	password = kw['password'],
	db = kw['db'],
	charset = kw.get('charset','utf8'),
	autocommit = kw.get('autocommit',True),
	maxsize = kw.get('maxsize',10),
	minsize = kw.get('minsize',1),
	loop = loop,
	)

async def select(sql,args,size=None):
	log(sql,args)
	global __pool
	async with __pool.get() as conn:
		async with conn.cursor(aiomysql.DictCursor) as cur:
			await cur.execute(sql.replace('?','%s'),args or ())
			if size:
				rs =await cur.fetchmany(size)
			else:
				rs =await cur.fetchall()

		logging.info('rows returned: %s'%len(rs))
		return rs

async def execute(sql,args):
	log(sql)
	global __pool
	async with __pool.get() as conn:
		try:
			async with conn.cursor() as cur:
				await cur.execute(sql.replace('?','%s'),args)
				affected = cur.rowcount
		except BaseException as e:
			raise
		return affected

def create_args_string(num):
	l=[]
	for i in range(num):
		l.append('?')
	return ','.join(l)

class Field(object):
	def __init__(self,name,column_type,primary_key,default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default
	def __str__(self):
		return '<%s,%s:%s>'%(self.__class__.__name__,self.column_type,self.name)

class StringField(Field):
	def __init__(self,name=None,primary_key=False,default=None,ddl='varchar(100)'):
		super().__init__(name,ddl,primary_key,default)

class IntegerField(Field):
	def __init__(self,name=None,primary_key=False,default=0,ddl='bigint'):
		super().__init__(name,ddl,primary_key,default)

class BooleanField(Field):
	def __init__(self,name=None,primary_key=False,default=False):
		super().__init__(name,'boolean',primary_key,default)

class FloatField(Field):
	def __init__(self,name=None,primary_key=False,default=0.0):
		super().__init__(name,'real',primary_key,default)

class TextField(Field):
	def __init__(self,name=None,primary_key=False,default=None):
		super().__init__(name,'text',primary_key,default)

class ModelMetaclass(type):
	def __new__(cls,name,bases,attrs):
		if name == 'Model':
			return type.__new__(cls,name,bases,attrs)
		tableName = attrs.get('__table__',None) or name
		logging.info('found Model %s(table:%s)'%(name,tableName))
		mappings = dict()
		fields = []
		primaryKey = None
		for k,v in attrs.items():
			if isinstance(v,Field):
				logging.info('found mapping: %s ==> %s'%(k,v) )
				mappings[k] = v
				if v.primary_key:
					if primaryKey:
						raise RuntimeError('duplicate primary key for field: %s'%k)
					primaryKey = k
				else:
					fields.append(k)
		if not primaryKey:
			raise RuntimeError('primary key not found')
		for k in mappings.keys():
			attrs.pop(k)
		escaped_fields = list(map(lambda f:'%s'%f,fields))
		attrs['__mappings__'] = mappings
		attrs['__table__'] = tableName
		attrs['__primary_key__'] = primaryKey
		attrs['__fields__'] = fields
		attrs['__select__'] = 'select %s,%s from %s'%(primaryKey,','.join(escaped_fields),tableName)
		attrs['__insert__'] = 'insert into %s(%s,%s) values(%s)' % (tableName,','.join(escaped_fields),primaryKey,create_args_string(len(escaped_fields)+1))
		attrs['__update__'] = 'update %s set %s where %s=?'%(tableName,','.join(map(lambda f: '%s=?'%(mappings.get(f).name or f),fields)),primaryKey)
		attrs['__delete__'] = 'delete from %s where %s=?' % (tableName,primaryKey)
		return type.__new__(cls,name,bases,attrs)

class Model(dict,metaclass=ModelMetaclass):
	def __init__(self,**kw):
		super(Model,self).__init__(**kw)
	def __getattr__(self,key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r"'Model' object has no attribute '%s'"%key)
	def __setattr__(self,key,value):
		self[key] = value
	def getValue(self,key):
		return getattr(self,key,None)
	def getValueOrDefault(self,key):
		value = getattr(self,key,None)
		if value is None:
			field = self.__mappings__[key]
			if field.default is not None:
				value = field.default() if callable(field.default) else field.default
				logging.debug('use default value for %s: %s'%(key,str(value)))
				setattr(self,key,value)
		return value
	
	@classmethod
	async def find(cls,pk):
		' find object by primary key. '
		rs = await select('%s where %s=?' % (cls.__select__,cls.__primary_key__),[pk],1)
		if len(rs) == 0:
			return None
		return cls(**rs[0])
	
	@classmethod
	async def findAll(cls,where=None,args=None,**kw):
		'find objects by where clause.'
		sql = [cls.__select__]
		if where:
			sql.append('where')
			sql.append(where)
		if args is None:
			args =[]
		orderBy = kw.get('orderBy',None)
		if orderBy:
			sql.append('order by')
			sql.append(orderBy)
		limit = kw.get('limit',None)
		if limit is not None:
			sql.append('limit')
			if isinstance(limit,int):
				sql.append('?')
				args.append(limit)
			elif isinstance(limit,tuple) and len(limit) == 2:
				sql.append('?,?')
				args.extend(limit)
			else:
				raise ValueError('Invalid limit value: %s' % str(limit))
		rs = await select(' '.join(sql),args)
		return [cls(**r) for r in rs]
	

	async def save(self):
		args = list(map(self.getValueOrDefault,self.__fields__))
		args.append(self.getValueOrDefault(self.__primary_key__))
		rows = await execute(self.__insert__,args)
		if rows != 1:
			logging.warn('failed to insert record:affected rows:%s'%rows)

if __name__ == '__main__':
	class User(Model):
		__table__ = 'Users'
		id = IntegerField(primary_key=True)
		name = StringField()

	loop = asyncio.get_event_loop()
	loop.run_until_complete(create_pool(loop,user='root',password='z5827468',db='test'))
	user = User(id=456,name='David') 
	loop.run_until_complete(user.save())
	loop.close()