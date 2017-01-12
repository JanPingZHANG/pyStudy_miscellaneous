from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

# get all internal links of the page 
def getInternalLinks(bsObj,includeUrl):
	includeUrl=urlparse(includeUrl).scheme+"://" + urlparse(includeUrl).netloc
	internalLinks=[]
	# find all begin with / links
	for link in bsObj.findAll("a",href=re.compile("^(/(?!/)|.*"+includeUrl+")")): 
		href=link.attrs['href']
		if href is not None:
			if href not in internalLinks:
				if href.startswith("/"):
					internalLinks.append(includeUrl+href)
				else :
					internalLinks.append(href)
	return internalLinks

# get all external links of the page
def getExternalLinks(bsObj,excludeUrl):
	externalLinks=[]
	# find all links begin with "http" or "www" and not contain current URL
	for link in bsObj.findAll("a",href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
		if link.attrs['href'] is not None:
			if link.attrs['href'] not in externalLinks:
				externalLinks.append(link.attrs['href'])
	return externalLinks

def getRandomExternalLink(startingPage):
	html=urlopen(startingPage)
	bsObj=BeautifulSoup(html,'lxml')
	externalLinks=getExternalLinks(bsObj,urlparse(startingPage).netloc)
	if len(externalLinks)==0 :
		print("No external links,looking around the site for one")
		domain=urlparse(startingPage).scheme+"://"+urlparse(startingPage).netloc
		internalLinks=getInternalLinks(bsObj,domain)
		return getRandomExternalLink(internalLinks[random.randint(0,len(internalLinks)-1)])
	else :
		return externalLinks[random.randint(0,len(externalLinks)-1)]

def followExternalOnly(startingSite):
	externalLink=getRandomExternalLink(startingSite)
	print("Rndom external link is "+externalLink)
	followExternalOnly(externalLink)

def splitAddress(address):
	addressParts=address.replace("http://","").split("/")
	return addressParts
allExtLinks=set()
allIntLinks=set()
def getAllExternalLinks(siteUrl):
	html=urlopen(siteUrl)
	bsObj=BeautifulSoup(html,'lxml')
	excludeUrl= urlparse(siteUrl).netloc
	externalLinks=getExternalLinks(bsObj,excludeUrl)
	internalLinks=getInternalLinks(bsObj,urlparse(siteUrl).scheme+"://"+urlparse(siteUrl).netloc)
	#externalLinks=getExternalLinks(bsObj,splitAddress(siteUrl)[(0)])
	#internalLinks=getInternalLinks(bsObj,splitAddress(siteUrl)[(0)])
	for link in externalLinks:
		if link not in allExtLinks:
			print(link)
			allExtLinks.add(link)
	for link in internalLinks:
		if link not in allIntLinks:
			print("URL is obtained "+ link)
			allIntLinks.add(link)
			getAllExternalLinks(link) 
getAllExternalLinks("http://oreilly.com")

