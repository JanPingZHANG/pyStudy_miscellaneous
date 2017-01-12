from multiprocessing import Pool
import os,time,random

def long_time_task(name):
	print 'start task %s %s'%(name,os.getpid())
	start=time.time()
	time.sleep(random.random() * 3)
	end=time.time()
	print 'finish task %s spend %0.2f'%(name,end-start)

if __name__=='__main__':
	print 'parent process is %s'%os.getpid()
	p=Pool(4)
	for i in range(5):
		p.apply_async(long_time_task,args=(i,))
	print 'waiting all task end'
	p.close()
	p.join()
	print 'all task DONE'
