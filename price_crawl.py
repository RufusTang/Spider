# -*- coding: utf-8 -*-

import urllib2
import re
from bs4 import BeautifulSoup

import csv
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import  xdrlib
import xlrd


def excel_table_byindex(file= 'file.xls',colnameindex=1,by_index=0):
    try:
        data = xlrd.open_workbook(file)
        table = data.sheets()[by_index]
        nrows = table.nrows
        ncols = table.ncols
        list =[[0 for ncol in range(ncols)] for row in range(nrows)]
        for i in range(nrows):
            row = table.row_values(i)
            for j in range(ncols):
                list[i][j] = row[j]
        return list
    except Exception,e:
        print str(e)

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
    UrlLinks =excel_table_byindex('UrlLinks.xlsx')
    Stock_Crawl_Results=[]
    for i in range(len(UrlLinks)):
        print UrlLinks[i][1]
        html = urllib2.urlopen(UrlLinks[i][1]).read()
        result = beautiful_soup_scraper(html)
        Stock_Crawl_Results.append(result)

    print Stock_Crawl_Results


    Csv_Data = []
    for i in range(len(Stock_Crawl_Results)):
        Csv_Data.append([Stock_Crawl_Results[i]['name'],Stock_Crawl_Results[i]['code'],Stock_Crawl_Results[i]['price']])

    csvfile = file('csvtest.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerows(Csv_Data)

if __name__ == '__main__':
    main()
