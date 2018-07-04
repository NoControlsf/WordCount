
import csv as csv
import random

import numpy as np

# -------------
# pandas读取cvs表格数据
# -------------
import pandas as pd
#df = pd.read_csv('E:/AI/data/answers.csv', encoding='gb18030')  # 读取answers的CSV的表格数据

#dd = pd.read_csv('E:/AI/data/questions.csv', encoding='gb18030')  # 读取questions的CSV的表格数据

#data = pd.merge(df, dd, on='que_id', how='left')  # pandas处理数据 找出索引关键字
#data = data[['que_id', 'ques_content', 'ans_content']]

# -------------
# pandas写入表格数据
# -------------
#data.to_csv(r'data.csv', encoding='gb18030')



def get_questions():
    data = []
    with open('E:/AI/data/questions.csv', 'r', newline='', encoding='gb18030') as f:
        for line in f.readlines():
            ru = line.strip().replace(' ', '')
            data.append(ru)
    return data

def get_answers():
    data = []
    with open('E:/AI/data/answers.csv', 'r', newline='', encoding='gb18030') as f:
        for line in f.readlines():
            ru = line.strip().replace(' ', '')
            data.append(ru)
    return data

data = get_questions()
question_list = []
for tmp in data[1:]:
    question_tmp = {}
    question_tmp['que_id'] = tmp.split(',')[0]
    question_tmp['ques_content'] = tmp.split(',')[1]
    print(question_tmp)
    question_list.append(question_tmp)


data2 = get_answers()
answer_list = []
for tmp in data2[1:]:
    answer_tmp = {}
    answer_tmp['que_id'] = tmp.split(',')[0]
    answer_tmp['ans_content'] = tmp.split(',')[1]
    print(answer_tmp)
    answer_list.append(answer_tmp)




final_result = []

for tmp in question_list:
    count = 0
    right_answer = []
    error_answer = []
    for tmpa in answer_list:
        if tmp['que_id'] == tmpa['que_id']:
            right_answer.append(tmpa['ans_content'])
            count += 1
        else:
            error_answer.append(tmpa['ans_content'])
    #没有答案跳过
    if count != 0:
        #正确答案
        for i in range(count):
            tmp_result = []
            tmp_result.append(1)
            tmp_result.append(tmp['que_id'])
            tmp_result.append(tmp['ques_content'])
            tmp_result.append(right_answer[i])
            final_result.append(tmp_result)

        #随机抽取错误答案样本
        error_list = random.sample(error_answer, count*5)
        for tmpe in error_list:
            tmp_result = []
            tmp_result.append(0)
            tmp_result.append(tmp['que_id'])
            tmp_result.append(tmp['ques_content'])
            tmp_result.append(tmpe)
            final_result.append(tmp_result)


with open("E:/AI/data/result.csv", "w") as csvfile:
    writer = csv.writer(csvfile)

    #先写入columns_name
    writer.writerow(["lable", "que_id", "ques_content", "ans_content"])
    #写入多行用writerows
    writer.writerows(final_result)

