import re
from bs4 import BeautifulSoup
import requests
import sqlite3 as sqlite

#每日楼盘统计
def  judgeDate():
    URL = 'http://data.house.163.com/bj/housing/xx1/ALL/all/1/allDistrict/todayflat/desc/all/1.html?loopline=0'
    headers = {
        'Host': 'data.house.163.com',
        'user agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
    }
    wb_data = requests.get(URL, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    print(soup)
    span = soup.find('span', class_='time')  #获取整个标签
    # print(span)
    spanTime = span.get_text().strip()  #获取标签中的内容文本
    print(spanTime)
    # 查询数据库中的数据日期，如果已经存在不爬取
    db = sqlite.connect('e:/stock/fdcstock.db')
    cur = db.cursor()
    dateResults = cur.execute('select distinct statisticsDate from house163')
    dateResults_list = []
    for dateResult in dateResults:
        dateResults_list.append(dateResult[0])
    db.commit()
    db.close()
    print(dateResults_list)
    if len(dateResults_list):
        for dateResult in dateResults_list:
            print(dateResult)
            if dateResult != spanTime:
                Daily_real_estate()
                print('ok')
    else:
        Daily_real_estate()
        print('ok')

# 获取列表信息
def getMessage(soup, spanTime):
    table = soup.find('table', class_='daTb')
    # print(table)
    tr_list = table.find_all('tr')
    # print(tr_list)
    for tr in tr_list[3:]:
        # print(tr)
        target_td = []
        td_list = tr.find_all('td')
        ahref = td_list[1].find('a')
        # print(ahref['href'])
        target_td.append(ahref['href'])
        target_td.append(spanTime)
        target_td.append(td_list[1].get_text().replace('\n', ''))
        target_td.append(td_list[3].get_text())
        target_td.append(td_list[4].get_text())
        target_td.append(td_list[5].get_text())
        target_td.append(td_list[6].get_text().replace('\n', '').replace(' ', '').replace(',', ''))
        target_td.append(td_list[7].get_text().replace('\n', '').replace(' ', '').replace(',', ''))
        target_td.append(td_list[8].get_text())
        target_td.append(td_list[9].get_text())
        target_td.append(td_list[10].get_text())
        target_td.append(td_list[11].get_text())
        target_td.append(td_list[12].get_text().replace('\t', '').replace(' ', '').replace('\n', ''))
        print(target_td)

        sql = 'replace into house163 values({})'.format(('?,' * len(target_td))[:-1])
        conn = sqlite.connect("E:/stock/fdcstock.db")
        cur = conn.cursor()
        cur.execute(sql, target_td)
        conn.commit()
        conn.close()
# 如果是更新过的网页开始爬取
def Daily_real_estate():
    for a in range(85):
        URL = 'http://data.house.163.com/bj/housing/xx1/ALL/all/1/allDistrict/todayflat/desc/all/{}.html?loopline=0'.format(a)
        headers = {
            'Host': 'data.house.163.com',
            'user agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36'
                          ' (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        wb_data = requests.get(URL, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # print(soup)
        span = soup.find('span', class_='time')  #获取整个标签
        # print(span)
        spanTime = span.get_text().strip()  #获取标签中的内容文本
        print(spanTime)
        getMessage(soup, spanTime)


if __name__ == '__main__':
    judgeDate()


