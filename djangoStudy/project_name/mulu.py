import re
from random import choice

def GetQuestion():
	questions = []
	num = re.compile('[0-9]')
	with open('Mulu.txt') as f:
		for line in f:
			if re.compile('^[0-9]').match(str(line)):
				st = str(line)
				st = st.replace('.','')
				st = num.sub('',st)
				questions.append(st)
	return choice(questions)



