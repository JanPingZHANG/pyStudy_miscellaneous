from urllib.request import urlopen
from urllib.error import HTTPError,URLError
from bs4 import BeautifulSoup
def getTitle(url):
	try:
		html= urlopen(url)
	except (HTTPError, URLError) as e:
		print(str(e))
		return None
	try:
		bsObj = BeautifulSoup(html.read(),'lxml')
		title = bsObj.body.h1
	except AttributeError as e:
		print(str(e))
		return None
	return title
title = getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None :
	print("Title could not be found")
else :
	print(title)
