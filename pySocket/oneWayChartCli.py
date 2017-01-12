from socket import *
import sys
import select

HOST='localhost'
PORT=21567
ADDR=(HOST,PORT)
BUFSIZE=1024

cliSock=socket(AF_INET,SOCK_STREAM)
cliSock.connect(ADDR)
sockInput=[cliSock,sys.stdin]
while True:
	readyInput,readyOutput,readyException=select.select(sockInput,[],[])
	for indata in readyInput:
		if indata==cliSock:
			data=cliSock.recv(BUFSIZE)
			if not data:
				break
			print 'server: ',data
		else:
			data=raw_input()
			if not data:
				break
			cliSock.send(data)
	if not data:
		break

cliSock.close()
