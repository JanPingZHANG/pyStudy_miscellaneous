import threading
from time import ctime

class MyThread(threading.Thread):
	def __init__(self,func,args,name=''):
		threading.Thread.__init__(self)
		self.func=func
		self.args=args
		self.name=name
	
	def run(self):
		print 'start ',self.name,' at ',ctime()
		self.res=apply(self.func,self.args)
		print 'finished ',self.name,' at ',ctime()
	
	def getResult(self):
		return self.res

