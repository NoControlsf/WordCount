import json
import os


def eachFilePath(root):
    for dirpath, dirnames, filenames in os.walk(root):
        for filepath in filenames:
            # print(os.path.join(dirpath, filepath))
            str = os.path.join(dirpath, filepath)
            # if(str.endswith('股权出质.json')):
            if(str.endswith('动产抵押.json')):
                print(str)
                print("###########")
                openFile(str)


def openFile(filepath):
    if os.path.getsize(filepath):
        with open(filepath, 'r', encoding='utf8') as load_f:
            load_dict = json.load(load_f)
            print(load_dict)
            # for i in range(len(load_dict)):
                # print(load_dict[i]['操作'])



if __name__ == '__main__':
    # filePath = "E:\\tyc2\\北京西城区\\8家集团信息（包括子公司和子公司下一级）\\法尔胜泓昇集团有限公司\\企业年报.json"
    root = "E:\\tyc2\\北京西城区\\8家集团信息（包括子公司和子公司下一级）"
    # openFile(filePath)
    eachFilePath(root)