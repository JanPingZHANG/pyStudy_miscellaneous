from socket import *
import sys
import select
import thread
import re

HOST=''
PORT=21567
ADDR=(HOST,PORT)
BUFSIZE=1024

servSock = socket(AF_INET,SOCK_STREAM)
servSock.bind(ADDR)
servSock.listen(5)
sockInput = [servSock,sys.stdin]
clients = {}

def DealConnectioner(cliSock,addr):
	cliAddr='%s:%s'%(addr[0],addr[1])
	while True:
		data = cliSock.recv(BUFSIZE)
		if data=='quit':
			del clients[cliAddr]
			cliSock.close()
			print 'close ',cliAddr
			break
		elif re.match('^to:',data):
			(client,data)=data.split('#')
			client=client[3:].strip()
			if not clients.has_key(client):
				print client,' not exist'
			else:
				clients[client].send('%s to you: %s' % (client,data))

		else:
			for client in clients:
				clients[client].send('%s: %s' % (cliAddr,data))

while True:
	print 'waiting for connection...'
	try:
		cliSock,addr=servSock.accept()
	except KeyboardInterrupt as e:
		print '\n close server'
		break
	print 'connected from ',addr
	if not clients.has_key('%s:%s'%(addr[0],addr[1])):
		clients['%s:%s'%(addr[0],addr[1])]=cliSock
		thread.start_new_thread(DealConnectioner,(cliSock,addr,))

for client in clients:
	clients[client].close()
	
