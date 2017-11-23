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

def openFile(filepath):
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
                            load_dict[i]['股东及出资信息'][a]['登记序号'] = '江苏八家'
                            # print(load_dict[i]['股东及出资信息'][a])
                            td_list2 = []
                            if(load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)']==None):
                                load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'] = 0
                            if(load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)']==None):
                                load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'] = 0
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['股东'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['认缴出资额(万元)'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['认缴出资时间'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['认缴出资方式'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['实缴出资额(万元)'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['实缴出资时间'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['实缴出资方式'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['年份'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['企业名称'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['统一社会信用代码'])
                            td_list2.append(load_dict[i]['股东及出资信息'][a]['登记序号'])

                            sql = 'replace into jsbjgd values({})'.format(('?,' * len(td_list2))[:-1])
                            print(sql)
                            conn = sqlite.connect("E:/stock/fdcstock.db")
                            cur = conn.cursor()
                            cur.execute(sql, td_list2)
                            conn.commit()
                            conn.close()

            # print(load_dict[i]['企业基本信息']['统一社会信用代码'])
            # print(load_dict[i]['年度'])

def eachFilePath(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            # print(os.path.join(dirpath, filepath))
            str = os.path.join(dirpath, filepath)
            if(str.endswith('企业年报.json')):
                print(str)
                print("###########")
                openFile(str)
                # openFile1(str)


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
                            load_dict[i]['对外投资信息'][a]['登记序号'] = '江苏八家'
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

if __name__ == '__main__':
    # filePath = "E:\\tyc2\\北京西城区\\8家集团信息（包括子公司和子公司下一级）\\法尔胜泓昇集团有限公司\\企业年报.json"
    root = "E:\\tyc2\\北京西城区\\8家集团信息（包括子公司和子公司下一级）"
    # openFile(filePath)
    eachFilePath(root)