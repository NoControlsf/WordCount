import requests
from bs4 import BeautifulSoup   #它是一个工具箱，通过解析文档为用户提供需要抓取的数据
import sqlite3 as sqlite
import time
from Tools import Time

#判断当前页面数据是否已经入库

def  judgeDate():
    url = 'http://data.house.163.com/bj/housing/xx1/ALL/all/{0}-{1}/allDistrict/todayflat/desc/all/1.html?loopline=0'.format(date, date)
    headers = {
    'Host': 'data.house.163.com',
    'user agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36'
                ' (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
       }
    wb_data = requests.get(url, headers=headers)
    #time.sleep(2)               # 设置爬取数据休眠时间（单位:秒），防止爬取的网站终止连接
    soup = BeautifulSoup(wb_data.text, 'lxml')   #lxml解析HTML页面
    # print(soup)
    span = soup.find('span', class_='time')      #获取整个标签
    # print(span)
    spanTime = span.get_text()                   #获取标签中的内容文本
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
            if dateResult != spanTime.strip():
                Date_parameter_estate()
    else:
        Date_parameter_estate()                          #执行爬取数据程序


#爬取从开始日期到截止日期整个时间段内每一天的数据

def Date_parameter_estate():

    for pag in range(85):
        time.sleep(20)               # 设置爬取数据休眠时间（单位:秒），防止爬取的网站终止连接
        # 交互式获取日期参数
        url = 'http://data.house.163.com/bj/housing/xx1/ALL/all/{0}-{1}/allDistrict/todayflat/desc/all/{2}.html?loopline=0'.format(date, date, pag+1)

        headers = {
            'Host': 'data.house.163.com',
            'user agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        wb_data = requests.get(url, headers=headers)  # 发请求
        soup = BeautifulSoup(wb_data.text, 'lxml')
        # print(soup)
        span = soup.find('span', class_='time')
        # print(span)                                 # <span class="time"> 2017.12.09 </span>
        spanTime = span.get_text()                    # 获取标签中的内容文本
        # print(spanTime)
        getMessage(soup, spanTime)

        # 获取列表信息
def getMessage(soup, spanTime):

        table = soup.find('table', class_='daTb')
        # print(table)
        tr_list = table.find_all('tr')                #在table中找出所有的tr标签
        # print(tr_list)
        for tr in tr_list[3:]:
            # print(tr)
            target_td = []
            td_list = tr.find_all('td')
            # print(td_list)
            ahref = td_list[1].find('a')
            # print(ahref['href'])
            target_td.append(ahref['href'])
            target_td.append(spanTime.strip())
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

if __name__ == '__main__':
    for date in Time.dateRange('startDate', 'ClosingDate'):
        # print(date)
        judgeDate()
        # print(date.split('.')[0]+"年"+ date.split('.')[1]+"月"+ date.split('.')[2]+"日")
