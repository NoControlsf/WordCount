# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import time
import sqlite3 as sqlite
import pymysql

# 沪深A股
def HS_A_Shares():
        url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._A&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=3480&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.8564695915729554"
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        reg = re.compile(r"(?<=\=)\S+")  # 匹配冒号后的字符串
        str = reg.search(soup.find('p').get_text()).group(0)
        sList = re.findall(r'[^\[\]]+', str)[1]   # 匹配方括号的字符串
        list = re.split('","', sList)  # 将字符串转化成列表
        pList = []
        for tmp in list:
            pList.append(tmp.replace('"', ''))  # 处理多余的双引号
        # print(pList)
        for msg in pList:
            msgList = re.split(',', msg)
            del msgList[0]  # 删除序号
            for a in range(8):
                del msgList[12]  # 删除多余字段
            fList = []
            for tmp in msgList:
                if tmp == '-':
                    fList.append('')  # 如果为横线则为空
                else:
                    fList.append(tmp)
            today = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))  # 获取当天的时间
            fList.append(today)
            if fList[14] != '':
                fList[14] += '%'
            # 处理数字为空
            if fList[2] == '':
                fList[2] = '0'
            if fList[3] == '':
                fList[3] = '0'
            if fList[5] == '':
                fList[5] = '0'
            if fList[6] == '':
                fList[6] = '0'
            if fList[7] == '':
                fList[7] = '0'
            if fList[8] == '':
                fList[8] = '0'
            if fList[9] == '':
                fList[9] = '0'
            if fList[10] == '':
                fList[10] = '0'
            if fList[11] == '':
                fList[11] = '0'
            if fList[13] == '':
                fList[13] = '0'
            if fList[15] == '':
                fList[15] = '0'
            # 股票代码 名称 最新价 涨跌额 涨跌幅 振幅 成交量（手） 成交额 昨收 今开 最高 最低 5分钟涨跌 量比 换手 市盈率（动）日期
            print(fList)
            # mysql
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='shares',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cur = conn.cursor()
            sql = 'insert into HSAShares values({})'.format(('\"%s\",' * len(fList))[:-1])
            # print(sql)
            cur.execute(sql % tuple(fList))
            cur.close()
            conn.commit()
            conn.close()
            # sqlite
            # sql = 'replace into HSSharesA values({})'.format(('?,' * len(fList))[:-1])
            # conn = sqlite.connect("E:/stock/Shares.db")
            # cur = conn.cursor()
            # cur.execute(sql, fList)
            # conn.commit()
            # conn.close()


# 港股
def HK_Shares():
        url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._HKS&sty=FCOQB&sortType=C&sortRule=-1&page=1&pageSize=2140&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.20960701247525315"
        wb_data = requests.get(url)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        sList = re.findall(r"[^\[\]]+", soup.get_text())[1]   # 匹配方括号的字符串
        list = re.split('","', sList)  # 将字符串转化成列表
        pList = []
        for tmp in list:
            pList.append(tmp.replace('"', ''))  # 处理多余的双引号
        # print(pList)
        for msg in pList:
            msgList = re.split(',', msg)
            msgList.pop()
            msgList.pop()
            fList = []
            for tmp in msgList:
                if tmp == '-':
                    fList.append('')  # 如果为横线则为空
                else:
                    fList.append(tmp)
            # 处理数字为空
            if fList[2] == '':
                fList[2] = '0'
            if fList[3] == '':
                fList[3] = '0'
            if fList[5] == '':
                fList[5] = '0'
            if fList[6] == '':
                fList[6] = '0'
            if fList[7] == '':
                fList[7] = '0'
            if fList[8] == '':
                fList[8] = '0'
            if fList[9] == '':
                fList[9] = '0'
            if fList[10] == '':
                fList[10] = '0'
            print(fList)
            # 股票代码 名称 最新价 涨跌额 涨跌幅 成交量(股) 成交额(港元) 今开 最高 最低 昨收 时间
            # mysql
            conn = pymysql.connect(
                host='localhost',
                port=3306,
                user='root',
                passwd='',
                db='shares',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            cur = conn.cursor()
            sql = 'insert into HKShares values({})'.format(('\"%s\",' * len(fList))[:-1])
            # print(sql)
            cur.execute(sql % tuple(fList))
            cur.close()
            conn.commit()
            conn.close()
            # sqlite
            # sql = 'replace into HKShares values({})'.format(('?,' * len(fList))[:-1])
            # conn = sqlite.connect("E:/stock/Shares.db")
            # cur = conn.cursor()
            # cur.execute(sql, fList)
            # conn.commit()
            # conn.close()

# 美股
def US_Shares():
    url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._UNS&sty=MPICTTA&sortType=C&sortRule=-1&page=1&pageSize=5500&js=var%20quote_123%3d{rank:[(x)],pages:(pc)}&token=44c9d251add88e27b65ed86506f6e5da&jsName=quote_123&_g=0.8786660780982527"
    wb_data = requests.get(url)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    sList = re.findall(r"[^\[\]]+", soup.get_text())[1]   # 匹配方括号的字符串
    list = re.split('","', sList)  # 将字符串转化成列表
    pList = []
    for tmp in list:
        pList.append(tmp.replace('"', ''))  # 处理多余的双引号
    # print(pList)
    for msg in pList:
        msgList = re.split(',', msg)
        msgList.pop()
        # 去除不明确的字段
        del msgList[0]
        del msgList[12]
        del msgList[12]
        del msgList[14]
        del msgList[14]
        del msgList[14]
        del msgList[16]
        del msgList[16]
        del msgList[18]
        del msgList[19]
        del msgList[19]
        for a in range(9):
            del msgList[20]
        fList = []
        for tmp in msgList:
            if tmp == '-':
                fList.append('')  # 如果为横线则为空
            else:
                fList.append(tmp)
        # 处理数字为空
        if fList[2] == '':
            fList[2] = '0'
        if fList[3] == '':
            fList[3] = '0'
        if fList[4] == '':
            fList[4] = '0'
        if fList[5] == '':
            fList[5] = '0'
        if fList[8] == '':
            fList[8] = '0'
        if fList[9] == '':
            fList[9] = '0'
        if fList[10] == '':
            fList[10] = '0'
        if fList[11] == '':
            fList[11] = '0'
        if fList[12] == '':
            fList[12] = '0'
        if fList[13] == '':
            fList[13] = '0'
        if fList[14] == '':
            fList[14] = '0'
        if fList[15] == '':
            fList[15] = '0'
        if fList[16] == '':
            fList[16] = '0'
        if fList[17] == '':
            fList[17] = '0'
        if fList[19] == '':
            fList[19] = '0'
        if fList[20] == '':
            fList[20] = '0'
        print(fList)
        # （美股的报价单位全部按美元） 简称 名称 今开 昨收 最新价 涨跌额 涨跌幅 换手率 最高价 最低价 成交量 成交额 外盘 内盘 总股本 总市值 市净率 收益(动) 时间 每股净资产 均价
        # mysql
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='',
            db='shares',
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        cur = conn.cursor()
        sql = 'insert into USShares values({})'.format(('\"%s\",' * len(fList))[:-1])
        # print(sql)
        cur.execute(sql % tuple(fList))
        cur.close()
        conn.commit()
        conn.close()
        # sql = 'replace into USShares values({})'.format(('?,' * len(fList))[:-1])
        # conn = sqlite.connect("E:/stock/Shares.db")
        # cur = conn.cursor()
        # cur.execute(sql, fList)
        # conn.commit()
        # conn.close()

if __name__ == '__main__':
    # HS_A_Shares()  # 沪深A股
    HK_Shares()  # 港股
    US_Shares()  # 美股