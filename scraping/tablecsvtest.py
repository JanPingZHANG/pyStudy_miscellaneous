import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bsObj = BeautifulSoup(html)
table = bsObj.findAll('table',{'class':'wikitable'})[0]
rows = table.findAll('tr')
csvfile = open('tabletest.csv','wt',newline='',encoding='utf-8')
writer = csv.writer(csvfile)
try:
	for row in rows:
		csvRow = []
		for cell in row.findAll(['td','th']):
			csvRow.append(cell)
		writer.writerow(csvRow)
finally:
	csvfile.close()
