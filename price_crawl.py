# -*- coding: utf-8 -*-


import csv
import urllib2
import re
from bs4 import BeautifulSoup


import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


pattern = re.compile('\'(.*)\'')
def beautiful_soup_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    stock_info = {}
    for result in soup.findAll('script'):
        if result.text.find(r'window.stock_info') !=-1:
            stock_info['name'] = pattern.findall(result.text.replace(' ','').split('\n')[2])[0]
            stock_info['code'] = pattern.findall(result.text.replace(' ', '').split('\n')[3])[0]
            stock_info['price'] = pattern.findall(result.text.replace(' ','').split('\n')[4])[0]
            return stock_info
    return "Not Found"

def main():
    html = urllib2.urlopen('http://quotes.money.163.com/0600019.html').read()
    result = beautiful_soup_scraper(html)
    csvfile = file('csvtest.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow([result['name'], result['code'], result['price']])

if __name__ == '__main__':
    main()
