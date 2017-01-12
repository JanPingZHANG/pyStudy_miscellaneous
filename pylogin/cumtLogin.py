import requests
from lxml import etree
import xml.etree.ElementTree as ET
from urllib import urlretrieve
from PIL import Image
import subprocess
import urllib
from selenium import webdriver
import time

headers = {
'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
'Host':'219.219.35.78',
'Origin':'http://219.219.35.78',
'Referer':'http://219.219.35.78/UserLogin.aspx?exit=1',
}

cumt = 'http://219.219.35.78/'
session = requests.Session()
html = session.get(cumt).content
#print html
tree = etree.HTML(html)
viewstate = tree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
#print viewstate
eventalidation=tree.xpath('//*[@id="__EVENTVALIDATION"]/@value')[0]
#print eventalidation
imagePath = tree.xpath('//*[@id="ValidateImage"]/@src')[0]
imagePath = cumt + imagePath
#urlretrieve(imagePath,'cumt.jpg')
cha = session.get(imagePath)
with open('cumt.jpg','wb') as imageFile:
	imageFile.write(cha.content)
p = subprocess.Popen(['tesseract','cumt.jpg','cumt'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
p.wait()
#im = Image.open('cumt.jpg')
#im.show()
#im.close()
f = open('cumt.txt','r')
validateCode = f.read()
f.close()
validateCode = validateCode.replace('\n','')
print 'ValidateCode is : ',validateCode

params = {
'ValidateCode':validateCode,
'ScriptManager1':'UpdatePanel2|btLogin',
'__EVENTTARGET':'btLogin',
'__EVENTARGUMENT': '',
'__LASTFOCUS': '', 
'__VIEWSTATE':viewstate,
'__VIEWSTATEGENERATOR':'7A1355CA',
'__EVENTVALIDATION':eventalidation,
'UserName':'TS15020183P2',
'PassWord':'19921213',
'drpLoginType': '1',
'__ASYNCPOST':'true',
}

req = session.post('http://219.219.35.78/UserLogin.aspx?exit=1',data=params,headers=headers)
#print req.content
s = session.get('http://219.219.35.78/Gstudent/topmenu.aspx?UID=TS15020183P2')

print s.content
#zhuce = session.get('http://219.219.35.78/Gstudent/TrainManage/StudentOnLineReg.aspx?EID=OAsxkCGom-SrCx3ttSxttpLh0ONY6Awb8D8HdbGr2NKtZaxYwou7Kh3xOsxtPMKQ&UID=TS15020183P2',headers=headers)
#print zhuce.content
#print session.post.__doc__
#print params
#print req.status_code
#print req.headers
#print req.cookies
#print req.request
#print req.encoding
#print req.reason
#print req.elapsed
