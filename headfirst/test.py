v='ten'
for case in switch(v):
	if case('one'):
		result=1
		break
	if case('ten'):
		result=10
		break
print(result)
