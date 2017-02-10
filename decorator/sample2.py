
def log(text):
	def decorator(func):
		def wrapper(*args,**kw):
			print('%s %s()'%(text,func.__name__))
			return func(*args,**kw)
		return wrapper
	return decorator

@log('execute')
def now():
	print('2017-01-17')

now()
a = log('execute')(now)
print('method name: ',a.__name__)


import functools
def log2(text):
	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args,**kw):
			print('%s %s()'%(text,func.__name__))
			return func(*args,**kw)
		return wrapper
	return decorator

@log2('execute')
def now2():
	print('2017-01-17')

b = log2('execute')(now2)
print('add functools.wraps: method name: ',b.__name__)
