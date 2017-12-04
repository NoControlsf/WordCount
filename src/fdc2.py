import re
import sqlite3 as sqlite

import requests

from bs4 import BeautifulSoup

import socket
import time
# 建设项目选址意见书

def building_name_approval():
    num_list = []
    for a in range(9622):
        num_list.append(a*10)
    for i in num_list:
        print(i)
        # url = 'http://www.bjghw.gov.cn/query/table7/index?pager.offset=950&s=1&qu=1'
        url = 'http://www.bjghw.gov.cn/query/table7/index?pager.offset={}&s=&qu='.format(i)
        headers = {
            'Host': 'www.bjghw.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'Cookie':'JSESSIONID=A67C9538F06661C58461EBB5C996C4AA; wzwsconfirm=cc11aa410af44879b105c1be7546238d; wzwstemplate=MTA=; ccpassport=2af7c9b30e9dcb05d9ecdfae6316b955; wzwschallenge=-1; wzwsvtime=1510120301; _va_id=6c7ad518eed8798d.1510030906.5.1510120924.1510120437.; _va_ses=*; _gscs_2055434732=t10120437ev7ok214|pv:2; _gscbrs_2055434732=1; _gscu_2055434732=10030906qpyuar14'
        }
        wb_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')

        reg = re.compile(r"(?<=\=)\S+")  # 匹配等号后的字符串
        detail_num_list = []
        table = soup.find('table', class_='box_main')

        table_list = table.find_all('table')
        tag_table = table_list[1]

        tr_list = tag_table.find_all('tr')
        for tr in tr_list[1:]:
            td_list = tr.find_all('td')
            td_list2 = []
            for td in td_list:
                td_list2.append(td.get_text())
                sa = td.find('a')
                if sa != None:
                    hr = str(sa['href'])
                    numb = reg.search(hr).group(0)
                    td_list2.pop()
                    td_list2.append(numb)
            print(td_list2)
            sql = 'replace into buildingNameApprovalList values({})'.format(('?,' * len(td_list2))[:-1])
            conn = sqlite.connect("E:/stock/fdcstock.db")
            # 建设单位 项目名称 发文号 立案号 id
            cur = conn.cursor()
            cur.execute(sql, td_list2)
            conn.commit()
            conn.close()
            detail_num = td_list2[4]
            detail_num_list.append(detail_num)
        print(detail_num_list)
        # for count in detail_num_list:
            # building_detail(count)

# 建设单位项目办理详细信息
def building_detail():
    col_id_list = []
    db = sqlite.connect('E:/stock/fdcstock.db')
    cur = db.cursor()
    results = cur.execute("select id from buildingNameApprovalList")
    for result in results.fetchall():
        col_id_list.append(result[0])
    db.commit()
    db.close()
    col_id_list1 = []
    db = sqlite.connect('E:/stock/fdcstock.db')
    cur = db.cursor()
    results = cur.execute("select id from buildingDetail")
    for result in results.fetchall():
        col_id_list1.append(result[0])
    db.commit()
    db.close()
    print(len(col_id_list1))
    for redata in col_id_list1:
        col_id_list.remove(redata)

    for count in col_id_list:
        print(count)
        detail_url = 'http://www.bjghw.gov.cn/query/table7/view?id={}'.format(count)
        headers = {
            'Host': 'www.bjghw.gov.cn',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'Cookie': 'JSESSIONID=C7C12332E453F2D015B5083E73644DB1'
        }

        timeout = 10
        socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
        sleep_download_time = 1
        time.sleep(sleep_download_time) #这里时间自己设定

        wb_data = requests.get(detail_url, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        table = soup.find('table', class_='box_main')
        tag_table = table.find('table')
        tr_list = tag_table.find_all('tr')
        #  建设单位 项目名称 建设位置 发文号 立案号 项目办理状态
        td_list2 = []
        td_list2.append(count)
        for tr in tr_list[1:]:
            td_list1 = tr.find_all('td')
            if td_list1 != None:
                td_list = tr.find_all('td')
                td_list2.append(td_list[1].get_text().replace('\r', '').replace('\n', '').replace(' ', ''))
        print(td_list2)
        sql = 'replace into buildingDetail values({})'.format(('?,' * len(td_list2))[:-1])
        conn = sqlite.connect("E:/stock/fdcstock.db")
        cur = conn.cursor()
        cur.execute(sql, td_list2)
        conn.commit()
        conn.close()


# 建筑名称核准
def building_name_check():
    num_list = []
    for a in range(215):
        num_list.append(a*10)
    for i in num_list:
        print(i)
        url = 'http://www.bjghw.gov.cn/query/table4/index?pager.offset={}&s=&qu='.format(i)
        headers = {
            'Host': 'www.bjghw.gov.cn',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'Cookie': 'JSESSIONID=0898720B2E9702A14D1C5E884512F973; _gscs_2055434732=11487404d182sd14|pv:1; _gscbrs_2055434732=1; _va_id=44ea5a4ca308e9de.1511487405.1.1511487951.1511487405.; _va_ses=*; _gscu_2055434732=114874041znvwh14'
        }
        wb_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        reg = re.compile(r"(?<=\=)\S+")  # 匹配等号后的字符串
        detail_num_list = []
        table = soup.find('table', class_='box_main')

        table_list = table.find_all('table')
        tag_table = table_list[1]

        tr_list = tag_table.find_all('tr')
        for tr in tr_list[1:]:
            td_list = tr.find_all('td')
            td_list2 = []
            for td in td_list:
                td_list2.append(td.get_text())
                sa = td.find('a')
                if sa != None:
                    hr = str(sa['href'])
                    numb = reg.search(hr).group(0)
                    td_list2.pop()
                    td_list2.append(numb)
            print(td_list2)
            # 申报单位 核准名称 详细地址 审批文号 id
            sql = 'replace into buildingNameCheckList values({})'.format(('?,' * len(td_list2))[:-1])
            conn = sqlite.connect("E:/stock/fdcstock.db")
            cur = conn.cursor()
            cur.execute(sql, td_list2)
            conn.commit()
            conn.close()
            detail_num = td_list2[4]
            detail_num_list.append(detail_num)
        print(detail_num_list)

# 建筑名称核准详细信息
def building_name_check_detail():
    col_id_list = []
    db = sqlite.connect('E:/stock/fdcstock.db')
    cur = db.cursor()
    results = cur.execute("select bid from buildingNameCheckList")
    for result in results.fetchall():
        col_id_list.append(result[0])
    db.commit()
    db.close()
    col_id_list1 = []
    db = sqlite.connect('E:/stock/fdcstock.db')
    cur = db.cursor()
    results = cur.execute("select bid from buildingNameCheckDetail")
    for result in results.fetchall():
        col_id_list1.append(result[0])
    db.commit()
    db.close()
    print(len(col_id_list1))
    for redata in col_id_list1:
        col_id_list.remove(redata)

    for count in col_id_list:
        print(count)
        detail_url = 'http://www.bjghw.gov.cn/query/table4/view?id={}'.format(count)
        headers = {
            'Host': 'www.bjghw.gov.cn',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'Cookie': 'JSESSIONID=0898720B2E9702A14D1C5E884512F973; _gscs_2055434732=11487404d182sd14|pv:1; _gscbrs_2055434732=1; _va_id=44ea5a4ca308e9de.1511487405.1.1511487951.1511487405.; _va_ses=*; _gscu_2055434732=114874041znvwh14'
        }

        timeout = 10
        socket.setdefaulttimeout(timeout)#这里对整个socket层设置超时时间。后续文件中如果再使用到socket，不必再设置
        sleep_download_time = 1
        time.sleep(sleep_download_time) #这里时间自己设定

        wb_data = requests.get(detail_url, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        table = soup.find('table', class_='box_main')
        tag_table = table.find('table')
        tr_list = tag_table.find_all('tr')
        #  申报单位 建设地区 详细地址 核准名称 审批文号 核发日期
        td_list2 = []
        td_list2.append(count)
        for tr in tr_list[1:]:
            td_list1 = tr.find_all('td')
            if td_list1 != None:
                td_list = tr.find_all('td')
                td_list2.append(td_list[1].get_text().replace('\r', '').replace('\n', '').replace(' ', ''))
        print(td_list2)
        sql = 'replace into buildingNameCheckDetail values({})'.format(('?,' * len(td_list2))[:-1])
        conn = sqlite.connect("E:/stock/fdcstock.db")
        cur = conn.cursor()
        cur.execute(sql, td_list2)
        conn.commit()
        conn.close()

if __name__ == '__main__':
    # building_name_approval()   # 先运行
    # building_detail()  # 从数据库里获取id，然后抓取
    # building_name_check()
    building_name_check_detail()


