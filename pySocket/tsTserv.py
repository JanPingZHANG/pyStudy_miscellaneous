from socket import *
from time import ctime
import sys
import thread

def receiveMessage(tcpCliSock):
	while True:
		data = tcpCliSock.recv(BUFSIZE)
		if not data:
			break
		print ' get a message: ',data

HOST=''
PORT=21567
if len(sys.argv)>1:
	PORT=int(sys.argv[1])
BUFSIZE=1024
ADDR=(HOST,PORT)
tcpSerSock=socket(AF_INET,SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
	print 'waiting for connection...'
	tcpCliSock,addr=tcpSerSock.accept()
	print '...connected from:',addr
	thread.start_new_thread(receiveMessage,(tcpCliSock,))
	while True:
		inputData = raw_input('message for send:')
		tcpCliSock.send('[%s] %s'%(ctime(),inputData))
		if not inputData:
			tcpCliSock.close()
			break

tcpSerSock.close()

