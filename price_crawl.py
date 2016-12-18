# -*- coding: utf-8 -*-

import csv
import urllib2
import re
from bs4 import BeautifulSoup

pattern = re.compile('\'(.*)\'')
def beautiful_soup_scraper(html):
    soup = BeautifulSoup(html, 'html.parser')
    stock_info = {}
    for result in soup.findAll('script'):
        if result.text.find(r'window.stock_info') !=-1:
            stock_info['name'] = pattern.findall(result.text.replace(' ','').split('\n')[2])[0]
            stock_info['code'] = pattern.findall(result.text.replace(' ', '').split('\n')[3])[0]
            stock_info['price'] = pattern.findall(result.text.replace(' ','').split('\n')[4])[0]
            print stock_info
            print stock_info['name']
            return stock_info
    return "Not Found"

"""    for field in FIELDS:
        results[field] = soup.find('table').find('tr', id='places_{}__row'.format(field)).find('td', class_='w2p_fw').text
    return results
"""

def main():
    html = urllib2.urlopen('http://quotes.money.163.com/0600019.html').read()
    result = beautiful_soup_scraper(html)

if __name__ == '__main__':
    main()
