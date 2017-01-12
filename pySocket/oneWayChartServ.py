from socket import *
import sys
import select

HOST=''
PORT=21567
ADDR=(HOST,PORT)
BUFSIZE=1024

servSock = socket(AF_INET,SOCK_STREAM)
servSock.bind(ADDR)
servSock.listen(5)
sockInput = [servSock,sys.stdin]
while True:
	print 'waiting for connection...'
	cliSock,addr=servSock.accept()
	print 'connected from ',addr
	sockInput.append(cliSock)
	while True:
		readyInput,readyOutput,readyException=select.select(sockInput,[],[])
		for indata in readyInput:
			if indata==cliSock:
				data = cliSock.recv(BUFSIZE)
				if not data:
					break
				print 'client: ',data
			else:
				data = raw_input()
				if not data:
					break
				cliSock.send(data)
		if not data:
			break
	cliSock.close()
