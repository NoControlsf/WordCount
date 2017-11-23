from bs4 import BeautifulSoup
import requests
#Files
#To open a file in Python we use the open() funnction
#利用python阅读文件
"""
f = open("C:/Users/NoControl/Desktop/大数据工作/天眼查账号.txt", "r", encoding="utf-8")
g = f.read()
print(g)
f.close()

# 爬取别人博客上的内容
headers = {
    'Cookie': 'UM_distinctid=15e9902ab621b-00d157023f6b1a-1c107152-100200-15e9902ab641c1; CNZZDATA3347352=cnzz_eid%3D1805055668-1505803702-null%26ntime%3D1505803702; Hm_lvt_31deec06ac5374dcfa09b9686205ade7=1506491939; Hm_lpvt_31deec06ac5374dcfa09b9686205ade7=1506491939; __utma=226521935.701273129.1506491939.1506491939.1506491939.1; __utmc=226521935; __utmz=226521935.1506491939.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'
}

url = "http://www.cnblogs.com/harelion/p/5245762.html"
wb_data = requests.get(url)
soup = BeautifulSoup.get(wb_data.text, "lxml")
# paragraphs = soup.select('#cnblogs_post_body > p')
print(soup)

for paragraph in zip(paragraphs):
    data = {
        'paragraph': paragraph.get()
    }
    print(data)
"""

# python内置类型和Json进行转换
import json
data = {"spam": "foo", "parrot": 42}
in_json = json.dumps(data)  # Encode the data
print(in_json, type(in_json))
json.loads(in_json)  # Decode into a Python object
print(in_json, type(in_json))

dic1 = {'type': 'dic1', 'username': '测试', 'age': 16}
json_dic1 = json.dumps(dic1)
print(json_dic1, type(json_dic1))
json_dic2 = json.dumps(dic1, sort_keys=True, indent=4, separators=(',', ': '), ensure_ascii=True)
print(json_dic2, type(json_dic2))




