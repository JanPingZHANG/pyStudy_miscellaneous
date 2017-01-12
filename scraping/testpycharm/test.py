from urllib import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

conn = pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='z5827468',db='mysql',charset='utf8')
cur = conn.cursor()
random.seed(datetime.datetime.now())

def store(title,content):
    cur.execute('INSERT INTO pages(title,content) VALUES ("%s","%s")',(title,content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen('http://en.wikipedia.org'+articleUrl)
    bsObj = BeautifulSoup(html)
    title = bsObj.find('h1').get_text()
    content = bsObj.find('div',{'id':'mw-content-text'}).findAll('p').get_text()
    store(title,content)
    return bsObj.find('div',{'id':'bodyContent'}).findAll('a',href='^(/wiki/)((?!:).)*$')
