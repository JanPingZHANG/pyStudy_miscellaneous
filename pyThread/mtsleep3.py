import threading
from time import sleep,ctime

def loop(nloop,nsec):
	print 'start loop',nloop,' at: ',ctime()
	sleep(nsec)
	print 'loop',nloop,' done at: ',ctime()

loops=[2,4]

def main():
	nloops=range(len(loops))
	threads=[]
	for i in nloops:
		threads.append(threading.Thread(target=loop,args=(i,loops[i])))
	for i in nloops:
		threads[i].start()
	for i in nloops:
		threads[i].join()
	print 'all DONE at: ',ctime()

if __name__=='__main__':
	main()
