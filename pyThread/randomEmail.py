from random import randint
import re
import string
import random

def sourceString(upper=True,figure=True):
	sourceStr=''
	for word in string.lowercase:
		sourceStr=sourceStr+word
	if upper:
		for word in string.uppercase:
			sourceStr=sourceStr+word
	if figure:
		for i in range(10):
			sourceStr=sourceStr+str(i)
	return sourceStr		

def createEmail(length1,length2):
	sourceStr=sourceString(False)
	email=''
	for i in range(length1):
		email=email+random.choice(sourceStr)
	email=email+'@'
	for i in range(length2):
		email=email+random.choice(sourceStr)
	email=email+'.com'
	return email

def createWord(length):
	sourceStr=sourceString(False,False)
	word=''
	for i in range(length):
		word=word+random.choice(sourceStr)
	return word

def findEmails(txt):
	emails=re.findall('[a-z0-9A-Z.]+@[a-z0-9A-Z.]+com',txt)
	return emails


if __name__=='__main__':
	txt=''
	randNum=[0,1,2,3,4,5,6,6,8,9]
	count=0
	for i in range(60000):
		num=random.choice(randNum)
		if num==0:
			txt=txt+createEmail(randint(6,15),randint(3,7))+' '
		else:
			txt=txt+createWord(randint(3,16))+' '
		if i%5==0:
			txt=txt+'\n'
	with open('emailTxt.txt','w') as f:
		f.write(txt)
	#with open('emailTxt.txt','r') as f:
		#text=f.read()
	emails=findEmails(txt)
	print len(emails)
	#print emails
