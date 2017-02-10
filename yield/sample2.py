def accumulate():
	print('run accumulat')
	tally = 0
	while 1:
		next = yield
		if next is None:
			print('return a value:%s'%tally)
			return tally
		tally += next

def gather_tallies(tallies):
	print('run gather')
	while 1:
		tally = yield from accumulate()
		tallies.append(tally)

tallies = []
acc = gather_tallies(tallies)
#next(acc)
acc.send(None)

#for i in range(4):
#	acc.send(i)
#acc.send(None)
#for i in range(5):
#	acc.send(i)
#acc.send(None)
#print(tallies)
