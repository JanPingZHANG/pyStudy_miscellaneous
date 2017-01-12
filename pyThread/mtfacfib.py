from time import ctime,sleep
import threading
from myThread import MyThread

def fib(x):
	sleep(0.005)
	if x<2:
		return 1
	return (fib(x-2)+fib(x-1))

def fac(x):
	sleep(0.1)
	if x<2:
		return x
	return (x*fac(x-1))

def sum(x):
	sleep(0.1)
	if x<2:
		return x
	return (x+sum(x-1))

n=12
funcs=[fib,fac,sum]
nfuncs=range(len(funcs))
threads=[]
for i in nfuncs:
	t=MyThread(funcs[i],(n,),funcs[i].__name__)
	threads.append(t)
print 'starting main'
for i in nfuncs:
	threads[i].start()
for i in nfuncs:
	threads[i].join()
for i in nfuncs:
	print threads[i].getResult()
print 'all DONE'
