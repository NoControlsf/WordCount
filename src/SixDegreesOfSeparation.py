from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

def six_degrees_of_separation():
    html = urlopen("http://finance.sina.com.cn/")
    soup = BeautifulSoup(html)
    reg = re.compile(r"(?<=\=)\S+")  # 匹配等号后的字符串
    for link in soup.findAll("a"):
        if 'href' in link.attrs:
            print(link.attrs['href'])

if __name__ == '__main__':
    six_degrees_of_separation()