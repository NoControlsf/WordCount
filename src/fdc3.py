import re
import sqlite3 as sqlite
import urllib
import requests
import zlib
from bs4 import BeautifulSoup

import socket
import time


def construction_permission_information():
    num_list = []
    for a in range(1905):
        num_list.append(a+1)
    for i in num_list:
        print(i)
        url = 'http://www.bjjs.gov.cn/eportal/ui?pageId=308891'
        headers = {
            'Host': 'www.bjjs.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
        }
        values = {'currentPage': i,
                  'pageSize': 15}
        if values:
            postdata = urllib.parse.urlencode(values).encode('utf-8')
        else:
            postdata = None

        wb_data = requests.get(url, headers=headers, params=postdata)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        table = soup.find('table', class_='gridview')
        tdarr = table.find_all('td')
        for b in range(15):
            count = b*6
            tdarr2 = tdarr[count:count+6]
            print(tdarr2)



        time.sleep(10)


if __name__ == '__main__':
    construction_permission_information()