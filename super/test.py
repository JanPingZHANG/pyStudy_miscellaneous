class A:
	def __init__(self):
		print ('enter A')
		print ('leave A')

class B(A):
	def __init__(self):
		print ('enter B')
		super(B,self).__init__()
		print ('enter A')

b = B()
