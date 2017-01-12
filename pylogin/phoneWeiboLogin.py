import json
import base64
import requests

myWeiBo ={'su':'18252431988','sp':'z5827468'}

def getCookie(weibo):
	cookies = []
	loginURL = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
	account = weibo['su']
	password = weibo['sp']
	username = base64.b64encode(account.encode('utf-8')).decode('utf-8')
	postData = {
		'entry':'sso',
		'gateway':'1',
		'from':'null',
		'savestate':'0',
		'useticket':'0',
		'pagerefer':'',
		'vsnf':'1',
		'su':username,
		'service':'sso',
		'servertime':'1482824085',
		'nonce':'TN6Z3W',
		'pwencode':'rsa2',
		'rsakv':'1330428213',
		'sp':password,
		'sr':'1366*768',
		'encoding':'UTF-8',
		'cdult':'3',
		'domain':'sina.com.cn',
		'prelt':'51',
		'returntype':'TEXT',
	}
	session = requests.Session()	
	rep = session.post(loginURL,data=postData)
	cookie = rep.cookies.get_dict()
	print cookie
	print rep.content
	return cookie

#getCookie(myWeiBo)
cookie = 'SINAGLOBAL=120.195.97.112_1482651831.589850; Apache=39.155.186.70_1482715536.132472; SCF=AouzFDPczNvxnRG7i971FYI4Tu9TTE0pxDh0YeQCdSv-b_IMAIthw3Sp38m0B78EHfakP6KW9gkpfdtANJb_xnU.; U_TRS1=00000049.499a7c78.58608c65.3d356961; U_TRS2=00000049.49a77c78.58608c65.82ac049e; WEB2_APACHE2_YZ=d9f26ec119ae0fdccd8f566056496d91; bdshare_firstime=1482722431155; UOR=,my.sina.com.cn,; ULV=1482733400237:1:1:1:39.155.186.70_1482715536.132472:; SessionID=vfs3esb3njc0cn7e3j884n85h7; vjuids=-66939f3d1.1593a635d4a.0.24d390e6a9b5c; vjlast=1482743308.1482743308.30; ULOGIN_IMG=ja-a92ab30639b834c08ac1d15394db6b1578ae; SUB=_2A251ZlKODeRxGeRG6FYV9i_Ezz-IHXVWEsNGrDV_PUJbm9ANLWvCkW8pHfDHqGc97eARB8PwPACHlgu1VA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFI4nvjRNw.nRYdCpyDW57O5NHD95QE1heXShqp1hB0Ws4Dqcj6i--ci-zXi-iFi--fi-i8iK.Ni--Ni-zEi-i8i--fi-i2i-24i--fiK.0iKnNi--fiK.EiK.Xi--fiK.EiK.X; sso_info=v02m6alo5qztKWRk5yljpOQpZCToKWRk5iljoOgpZCjnLKOg4y0jYOYsY6DkLOJp5WpmYO0so6DjLSNg5ixjoOQsw=='
headers = {
	'Host':'my.sina.com.cn',
	#'Origin':'https://login.sina.com.cn',
	'Referer':'http://my.sina.com.cn/',
	'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Cookie':cookie,
	}

session = requests.Session()
rep = session.get('http://my.sina.com.cn/?',headers=headers)
print rep.content
