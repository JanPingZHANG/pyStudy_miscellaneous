def g(x):
	yield from range(x,0,-1)
	yield from range(x)

print (list(g(5)))
for i in g(5):
	print (i)
