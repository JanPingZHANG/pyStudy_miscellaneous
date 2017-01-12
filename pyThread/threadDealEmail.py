import threading
from Queue import Queue
from randomEmail import findEmails
from myThread import MyThread
from time import sleep

def readEmails(queue):
	s='start'
	with open('emailTxt.txt','r') as f:
		while s!='':
			s=f.readline()
			emails=findEmails(s)
			for email in emails:
				queue.put(email,1)
	queue.put('quit',1)

def writeEmails(queue):
	with open('emails.txt','w') as f:
		f.write('')
	while True:
		if queue.qsize()>0:
			email=queue.get()
			if email=='quit':
				break
			with open('emails.txt','a') as f:
				f.write(email+'\n')

def main():
	print 'starting...\n'
	q=Queue(100)
	funcs=[writeEmails,readEmails]
	nfuncs=range(len(funcs))
	threads=[]
	for i in nfuncs:
		t=MyThread(funcs[i],(q,),funcs[i].__name__)
		threads.append(t)
	for i in nfuncs:
		threads[i].start()
	for i in nfuncs:
		threads[i].join()
	print 'DONE'

if __name__=='__main__':
	main()
