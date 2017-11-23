from bs4 import BeautifulSoup

info = []
with open("C:/Users/NoControl/Desktop/沈阳双随机/demo_双随机/login.html", "r", encoding="UTF-8") as wb_data:
    Soup = BeautifulSoup(wb_data, "lxml")
#使用选择器从页面中抓取标签和标签中的内容
    divs = Soup.select("body > div ")
    images = Soup.select("#loginform > h2 > img")
    titles = Soup.select("#loginform > h2")
    # print(divs,images,titles,sep="\n===============\n")

#循环遍历获取内容
    for title, image, div in zip(titles, images, divs):
        data = {
            'title': title.get_text(),
            'div': div.get_text(),
            'image': image.get("src"),
            'number': 4
        }
        info.append(data)

# 筛选过滤信息
for i in info:
    if float(i['number']) > 3:
        print(i['title'], i['div'], i['image'])


"""
多行注释
python格式问题
地址url
css标签选择器
#loginform > h2 > img
"""





