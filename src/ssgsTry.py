import json

import requests
from bs4 import BeautifulSoup

url = 'http://www.cninfo.com.cn/cninfo-new/information/companylist'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')
div1 = soup.find('div', id='con-a-1')
div2 = soup.find('div', id='con-a-2')
div3 = soup.find('div', id='con-a-3')
div4 = soup.find('div', id='con-a-4')
div5 = soup.find('div', id='con-a-5')
div6 = soup.find('div', id='con-a-6')
for i in [1, 2, 3, 4, 5, 6]:
    div = soup.find('div', id='con-a-%d' % i)
    arr = []
    for a in div.find_all('a'):
        str = a.get_text()
        str1 = str.split(' ')[0]
        arr.append(str1)
    print(arr)
    # dict = {'dict%d' % i: arr}
    # with open("e:/stock/CNCode/div%d.json" % i, "w",  encoding='utf-8') as f:
        # json.dump(dict, f, ensure_ascii=False)
        # print("加载入文件完成...")