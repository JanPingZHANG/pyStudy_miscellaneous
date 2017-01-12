from twisted.internet import protocol,reactor

HOST = 'localhost'
PORT = 21567

class TSClntProtocol(protocol.Protocol):
	def SendData(self):
		data = raw_input('>')
		if data:
			print '...sending data %s...' % data
			self.transport.write(data)
		else:
			self.transport.loseConnection()

	def connectionMade(self):
		self.SendData()
	
	def dataReceived(self,data):
		print data
		self.SendData()
	
class TSClntFacotry(protocol.ClientFactory):
	protocol = TSClntProtocol
	clientConnectionLost = clientConnectionFailed = lambda self,connector,reason:reactor.stop()

reactor.connectTCP(HOST,PORT,TSClntFacotry())
reactor.run()
