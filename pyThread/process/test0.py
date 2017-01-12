import os

print 'starting in process %s'%os.getpid()
pid=os.fork()
if pid==0:
	print 'I (%s) am child process and my parent is %s'%(os.getpid(),os.getppid())
else :
	print 'I (%s) have child proces %s'%(os.getpid(),pid)
