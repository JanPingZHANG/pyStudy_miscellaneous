import threading
from time import ctime,sleep

class MyThread(threading.Thread):
	def __init__(self,func,args,name=''):
		threading.Thread.__init__(self)
		self.func=func
		self.args=args
		self.name=name
	
	def run(self):
		apply(self.func,self.args)

loops=[2,4]
def loop(nloop,nesc):
	print 'loop',nloop,' start at: ',ctime()
	sleep(nesc)
	print 'loop',nloop,' done at: ',ctime()

def main():
	print 'main starting at: ',ctime()
	threads=[]
	nloops=range(len(loops))
	for i in nloops:
		t = MyThread(loop,(i,loops[i]),loop.__name__)
		threads.append(t)
	for i in nloops:
		threads[i].start()
	for i in nloops:
		threads[i].join()
	print 'all Done at: ',ctime()

if __name__=='__main__':
	main()
