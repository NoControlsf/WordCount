# 1.urllib模块中的方法
# urllib.request.urlopen(url, data=None, [timeout,]*, cafile=None, capath=None, cadefault=False, context=None)
# - url:需要打开的网址
# - data: Post提交的数据
# - timeout: 设置网站的访问超时时间
# 直接用urllib.request模块的urlopen()获取页面，page的数据格式为bytes类型，需要decode()解码，转换成str类型
from urllib import error
from urllib import request, parse
"""
from urllib import request
"""
response = request.urlopen(r'http://www.baidu.com/')  #  <http.client.HTTPResponse object at 0x00000000048BC908>  HTTPResponse类型
page = response.read()
page = page.decode('utf-8')
# print(page)


"""
urlopen返回对象提供方法：
read(), readline(), readlines(), fileno(), close():对于HTTPResponse类型数据进行操作
info(): 返回HTTPMessage对象，表示远程服务器返回的头信息
getcode():返回Http状态码。如果是http请求，200请求成功完成;404网址未找到
geturl():返回请求的url
"""

# 2.使用Request
# urllib.request.Request(url, data=None, headers={}, method=None)
# 使用request() 来包装请求，再通过urlopen()获取页面
url = r'http://www.lagou.com/zhaopin/Python/?labelWords=label'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
req = request.Request(url, headers=headers)
page = request.urlopen(req).read()
page = page.decode('utf-8')
# print(page)

"""
用来包装头部的数据：
User-Agent: 这个头部可以携带如下几条信息：浏览器名和版本号，操作系统名和版本号。默认语言
Referer:可以用来防止盗链，有一些网站图片显示来源http://***.com,就是检查Referer来鉴定的
Connection:表示连接状态，记录Session的状态
"""

# 3.Post数据
# urllib.request.urlopen(url, data=None, [timeout]*, cafile=None, capath=None, cadefault=False,context=None)
# urlopen()的data参数默认为None,当data参数不为空的时候，urlopen()提交方式为Post
"""
url = r'http://www..lagou.com/jobs/positionAjax.json?'
headers = {
    'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
    'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
    'Connection': 'keep-alive'
}
data = {
    'first': 'true',
    'pn': 1,
    'kd': 'Python'
}
data = parse.urlencode(data).encode('utf-8')
req = request.Request(url, headers=headers, data=data)
page = request.urlopen(req).read()
page = page.decode('utf-8')
错误日志：
UnicodeError: encoding with 'idna' codec failed (UnicodeError: label empty or too long)
"""
"""
经过urlencode()转换后的data数据为?first=true?pn=1?kd=Python,
最后提交的url为http://www.lagou.com/jobs/positionAjax.json?first=true?pn=1?kd=Python
Post的数据必须是bytes或者iterable of bytes,不能是str,因此需要进行encode()编码
例： page = request.urlopen(req, data=data).read()
当然，也可以把data的数据封装在urlopen()参数中
"""

# 4.异常处理
def get_page(url):
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      r'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'Referer': r'http://www.lagou.com/zhaopin/Python/?labelWords=label',
        'Connection': 'keep-alive'
    }
    data = {
        'first': 'true',
        'pn': 1,
        'kd': 'Python'
    }
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, headers=headers)
    try:
        page = request.urlopen(req, data=data).read()
        page = page.decode('utf-8')
    except error.HTTPError as e:
        print(e.code())
        print(e.read().decode('utf-8'))
    return page

# 5.使用代理
# urllib.request.ProxyHandler(proxies=None)
# 当需要抓取的网站设置了访问限制，这时就需要用到代理来抓取数据


"""
data = {
        'first': 'true',
        'pn': 1,
        'kd': 'Python'
    }
proxy = request.ProxyHandler({'http': '5.22.195.215:80'})  # 设置proxy
opener = request.build_opener(proxy)  # 挂载opener
request.install_opener(opener)  # 安装opener
data = parse.urlencode(data).encode('utf-8')
page = opener.open(url, data).read()
page = page.decode('utf-8')
return page
"""
