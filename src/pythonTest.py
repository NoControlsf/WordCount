# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen
def catchAllInfoFromNet(myUrl):
    html = urlopen(myUrl).read().decode('utf-8', 'ignore')
    # print(html)
    # nameList = re.compile(r'<title>(.*?)</title>', re.DOTALL).findall(html)  # 列表形式
    # nameList = re.compile(r'href="(.*?)"', re.DOTALL).findall(html)  # 列表形式
    # nameList = re.compile(r'"name":"(.*?)"', re.DOTALL).findall(html)  # 列表形式
    nameList = re.compile(r'<p>(.*?)</p>', re.DOTALL).findall(html)  # 列表形式
    for i in range(0,len(nameList)):
        print("第%d个名字为：   %s" % (i, nameList[i]))
# 上一段源码是将字节转换成字符，这一点非常重要

# 对于如何下载网页：
# 这里有两种办法，一种如上面的代码所示，使用from urllib.request import urlopen 来直接
# 使用urlopen来抓取
# 第二种是使用urllib.request 来获取，代码如下：
import urllib.request
import re
def catchAllInfoFromNet(url):
    # 模拟浏览器，打开url
    headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/5'
                             '37.11 (KHTML,       like Gecko) Chrome/23.0.1271.64 Safari/537.11')
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    data = opener.open(url).read().decode('utf-8', 'ignore')
    nameList = re.compile(r'<p>(.*?)</p>', re.DOTALL).findall(data)  # 列表形式
    for i in range(0, len(nameList)):
        print("第%d个名字为：  %s" % (i, nameList[i]))
# 这种方式我们要伪装成浏览器进行网页抓取

# python程序中模拟网页登录，并且爬取网页:
import http.cookiejar
import urllib.request
import urllib
# 利用cookie模拟网站登录
filenameOfCookie = 'renren_cookie.txt'
cookie = http.cookiejar.MozillaCookieJar(filenameOfCookie)
headler = urllib.request.HTTPCookieProcessor
opener = urllib.request.build_opener(headler)
data = {"email": "18349366304", "password": "XXXXXXXXXXXX"}
postdata = urllib.parse.urlencode(data).encode(encoding='UTF-8')
loginurl = 'http://www.renren.com/PLogin.do'
request = opener.open(loginurl, postdata)
print(request)
cookie.save(ignore_discard=True,ignore_expires=True)
geturl = 'http://friend.renren.com/managefriends'
result = opener.open(geturl).read().decode('utf-8')
print(result)
filenameOfHtml = 'renren.html'
fileToWrite = open(filenameOfHtml, 'W')
fileToWrite.write(result)
fileToWrite.close()

# 我们首先使用了MozillaCookie等工具来创建了cookie之后创建了opener来承载
# 我们的处理引擎，之后就是重点了，我们伪造cookie的post数据，也就是data={"email":
# "18349366304", "passwoord": "XXXXXXXXXX"},因此我们就可以模拟输入账户密码登录了，
# 前面的工作就是为了这一步，经过一些编码处理后，我们通过request=opener.open(loginurl, postdata)
# 来真正的将这些信息应用到具体的数据包中，模拟浏览器进行登录，最后我们将获得的cookie信息保存起来，
# 写入文本文件中。并且为了测试，我们访问了一个不登录就不能访问的网页，抓取了这个网页的信息打印
# 并写入本地，程序结束。


# 如何攻破https格式的网页登录
# 这是首先是https协议，我们的fiddler
"""
from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
def getTitle(url):
        try:
            html = urlopen(url)
        except HTTPError as e:
            return None
        try:
            bsObj = BeautifulSoup(html.read())
            title = bsObj.body.h1
        except AttributeError as e:
            return None
        return title
        title = getTitle("http://pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found")
else:
    print(title)
"""

"""
html = urlopen("http://pythonscraping.com/pages/page1.html")
bsObj = BeautifulSoup(html.read(), 'lxml')
print(bsObj.h1)
# print(bsObj.nonExistentTag.someTag)
try:
    badContent = bsObj.nonExistingTag.antherTag
except AttributeError as e:
    print("Tag was not found")
else:
    if badContent == None:
        print("Tag was not found")
    else:
        print(badContent)
"""