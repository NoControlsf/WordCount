#-*- coding: UTF-8 -*-
# 年报信息清洗
'''
1、读取指定目录下的所有文件
2、读取指定文件，输出文件内容
3、创建一个文件并保存到指定目录
'''
import json
import os
import re
import sqlite3 as sqlite

import pymysql



def openFile(filepath, seq):
    if os.path.getsize(filepath):
        with open(filepath, 'r', encoding='utf8') as load_f:
            load_dict = json.load(load_f)
            for i in range(len(load_dict)):
                # print(load_dict[i]['股东及出资信息'])
                if(('股东及出资信息') in load_dict[i]):
                    if(load_dict[i]['股东及出资信息'] != None):
                        for a in range(len(load_dict[i]['股东及出资信息'])):
                            load_dict[i]['股东及出资信息'][a]['年份'] = re.findall(r'\d+', load_dict[i]['年度'])[0]
                            load_dict[i]['股东及出资信息'][a]['企业名称'] = load_dict[i]['企业基本信息']['企业名称']
                            load_dict[i]['股东及出资信息'][a]['统一社会信用代码'] = load_dict[i]['企业基本信息']['统一社会信用代码']
                            load_dict[i]['股东及出资信息'][a]['登记序号'] = '20180423爬取'
                            # print(load_dict[i]['股东及出资信息'][a])
                            td_list = []
                            td_list2 = []
                            rjcz = load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'].replace(' ', '')
                            if rjcz==None or rjcz == '':
                                load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'] = 0
                            else:
                                #print(rjcz)
                                rjcz_str = rjcz.replace('万元人民币', '').replace('万元', '')
                                try:
                                    rjcz_num = float(rjcz_str)
                                    load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'] = rjcz_num
                                except Exception:
                                    rjcz_num = 0
                                    load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'] = rjcz_num

                            sjcz = load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'].replace(' ', '')
                            if sjcz==None or sjcz == '':
                                load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'] = 0
                            else:
                                #print(sjcz)
                                sjcz_str = sjcz.replace('万元人民币', '').replace('万元', '')
                                try:
                                    sjcz_num = float(sjcz_str)
                                    load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'] = sjcz_num
                                except Exception:
                                    sjcz_num = 0
                                    load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'] = sjcz_num

                            td_list2.append(seq)

                            td_list2.append(load_dict[i]['股东及出资信息'][a]['登记序号'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['统一社会信用代码'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['年份'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['认缴出资方式'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['认缴出资时间'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['实缴出资时间'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['实缴出资方式'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['股东'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'])


                            #td_list2.append(load_dict[i]['股东及出资信息'][a]['企业名称'])


                            td_list.append(seq)
                            td_list.append(load_dict[i]['股东及出资信息'][a]['登记序号'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['统一社会信用代码'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['年份'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['企业名称'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['股东'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['认缴出资时间'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['认缴出资方式'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['实缴出资时间'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'])
                            td_list.append(load_dict[i]['股东及出资信息'][a]['实缴出资方式'])



                            """
                            sql = 'replace into jsbjgd values({})'.format(('?,' * len(td_list2))[:-1])
                            print(sql)
                            conn = sqlite.connect("E:/stock/fdcstock.db")
                            cur = conn.cursor()
                            cur.execute(sql, td_list2)
                            conn.commit()
                            conn.close()
                            """
                            print(td_list2)
                            print(td_list)
                            mysql_insert(td_list2)
                            mysql_insert2(td_list)
                            seq = seq + 1
    return seq
            # print(load_dict[i]['企业基本信息']['统一社会信用代码'])
            # print(load_dict[i]['年度'])

# 正文写入mysql数据库
def mysql_insert(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='shares',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = 'insert into P_ARSHAREHOLDER values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()

# 正文写入mysql数据库
def mysql_insert2(result_list):
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='123',
        db='shares',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = 'insert into P_OIESHAREHOLDER values({})'.format(('\"%s\",' * len(result_list))[:-1])
    # print(sql)
    cur.execute(sql % tuple(result_list))
    cur.close()
    conn.commit()
    conn.close()


def eachFilePath(root):
    seq = 310000
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            # print(os.path.join(dirpath, filepath))
            str = os.path.join(dirpath, filepath)
            if(str.endswith('企业年报.json')):
                print(str)
                print("###########")
                seq = openFile(str, seq)
                #openFile1(str)


def openFile1(filepath):
    if os.path.getsize(filepath):
        with open(filepath, 'r', encoding='utf8') as load_f:
            load_dict = json.load(load_f)
            for i in range(len(load_dict)):
                # print(load_dict[i]['股东及出资信息'])
                if(('对外投资信息') in load_dict[i]):
                    if(load_dict[i]['对外投资信息'] != None):
                        for a in range(len(load_dict[i]['对外投资信息'])):
                            load_dict[i]['对外投资信息'][a]['年份'] = re.findall(r'\d+', load_dict[i]['年度'])[0]
                            load_dict[i]['对外投资信息'][a]['企业名称'] = load_dict[i]['企业基本信息']['企业名称']
                            load_dict[i]['对外投资信息'][a]['统一社会信用代码'] = load_dict[i]['企业基本信息']['统一社会信用代码']
                            load_dict[i]['对外投资信息'][a]['登记序号'] = '20180423爬取'
                            # print(load_dict[i]['对外投资信息'][a])
                            td_list2 = []
                            td_list2.append(load_dict[i]['对外投资信息'][a]['统一社会信用代码/统一信用代码'])
                            td_list2.append(load_dict[i]['对外投资信息'][a]['对外投资企业名称'])
                            td_list2.append(load_dict[i]['对外投资信息'][a]['年份'])
                            td_list2.append(load_dict[i]['对外投资信息'][a]['企业名称'])
                            td_list2.append(load_dict[i]['对外投资信息'][a]['统一社会信用代码'])
                            td_list2.append(load_dict[i]['对外投资信息'][a]['登记序号'])

                            sql = 'replace into jsbjtz values({})'.format(('?,' * len(td_list2))[:-1])
                            print(sql)
                            conn = sqlite.connect("E:/stock/fdcstock.db")
                            cur = conn.cursor()
                            cur.execute(sql, td_list2)
                            conn.commit()
                            conn.close()

def countFilePath(root):
    count = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            # print(os.path.join(dirpath, filepath))
            str = os.path.join(dirpath, filepath)
            if(str.endswith('企业年报.json')):
                count += 1
    return count


if __name__ == '__main__':
    # filePath = "E:\\tyc2\\北京西城区\\8家集团信息（包括子公司和子公司下一级）\\法尔胜泓昇集团有限公司\\企业年报.json"
    root = "E:\\tyc\\yanshan"
    # openFile(filePath)

    eachFilePath(root)
    #count = countFilePath('f:/tyc/表2')
    #print(count)