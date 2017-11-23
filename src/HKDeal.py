from bs4 import BeautifulSoup
import requests
import re

headers = {
    'Cookie': 'TS0161f2e5=014125927681df22fe8484b732ab24bd66a7ebe27d09a5d54a55b1463036e2529d8877940e; TS01504d45=0141259276f247e8b6028e2122d751e88a88e566a0dc182a6cf188a1e0efee68dd065b1b05be45b04ed9dd4f6ce2df6512dc5aeadc; kanhanBase=sc.hkexnews.hk/TuniS/,www.hkexnews.hk; TS01e99ba5=0141259276e58f401ad8425509340ef83edb9f18c57474c7418a459c6dee93acfd1aa214b03c8a10e1cbf31cc51d1d45c877ec9a82',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
}
# 获取统一资源定位符
url = 'http://www.hkexnews.hk/listedco/listconews/mainindex/HOMEINDEX_c.HTM'
wb_data = requests.get(url)
wb_data.encoding = 'utf-8'
soup = BeautifulSoup(wb_data.text, 'lxml')
items = soup.select('body > table > tr > td > table > tr > td > table > tr > td')
pdfs = soup.select('body > table > tr > td > table > tr > td > table > tr > td > a')
print(items)
dr = re.compile(r'<[^>]+>', re.S)
for item in zip(items):
    data = {
        'title': dr.sub('', str(item))
    }
    print(data)

"""
爬取香港交易所最新上市公司公告
存在的问题：
1、table行内容存放到数组中的方式不对
2、信息用正则表达式处理过后还有一些符号的残余
3、a标签里的链接没有爬取出来
4、如何做到爬取代码的范用及代码的灵活性
"""