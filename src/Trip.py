from bs4 import BeautifulSoup
import requests

"""
# 获取url（统一资源定位符）
url = 'https://cn.tripadvisor.com/Attractions-g60763-Activities-New_York_City_New_York.html'
wb_data = requests.get(url)
soup = BeautifulSoup(wb_data.text, 'lxml')
# print(soup)
# titles = soup.select('#taplc_attraction_coverpage_attraction_0 > div > div > div > div.shelf_item_container > div > div.poi > div > div.item.name > a')
# imgs = soup.select('img[width="200"]')
# cates = soup.select('#taplc_attraction_coverpage_attraction_0 > div > div > div > div.shelf_item_container > div > div.poi > div > div > a')
titles = soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.listing_title > a')
imgs = soup.select('img[width="180"]')
cates = soup.select('#ATTR_ENTRY_ > div.attraction_clarity_cell > div > div > div.listing_info > div.tag_line > div > a > span')
# print(titles, imgs, cates, sep='\n=============\n')
for title, img, cate in zip(titles, imgs, cates):
    data = {
        'title': title.get_text(),
        'img': img.get('src'),
        'cate': list(cate.stripped_strings),
    }
    print(data)
"""

"""
<a href="/Attractions-g60763-Activities-c42-t224-New_York_City_New_York.html" data-params="clFBXy9BdHRyYWN0aW9ucy1nNjA3NjMtQWN0aXZpdGllcy1jNDItdDIyNC1OZXdfWW9ya19DaXR5X05ld19Zb3JrLmh0bWxfdUJz" onclick="ta.servlet.Attractions.narrow.setEvtCookieWrapper('Attraction_List_Click', 'Rollup_click', 'name', 16, 'VFdNXy9BdHRyYWN0aW9ucy1nNjA3NjMtQWN0aXZpdGllcy1jNDItdDIyNC1OZXdfWW9ya19DaXR5X05ld19Zb3JrLmh0bWxfQ1U3'); ta.call('ta.servlet.Attractions.narrow.ajaxifyLink', event, this)">城市游览 (206)</a>
<a href="/Attraction_Review-g60763-d143361-Reviews-Broadway-New_York_City_New_York.html" onclick="ta.setEvtCookie('Attraction_List_Click', 'POI_click', 'name', 9, '/Attraction_Review')" target="_blank">百老汇</a>
"""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
    'Coolie': 'TAUnique=%1%enc%3ATeiQuQ%2BEYjM4yzrpVBKI2rxxT%2FaE9LtXvQJpDJgQdwM2jHwltRJPGQ%3D%3D; TASSK=enc%3AAIeYMrAgkyGMrILiehaUhHa44N3Jh1dd9OuRIhqPgrEDcRQxr310N5sSFCvKea3nOdMjpqnxmZJE4J6AriGMEItjNPgv4bzFV6a61sujZLIqkG8ZVuEP3fBGE4ZfeBdQoA%3D%3D; TAPD=tripadvisor.cn; _jzqckmp=1; __gads=ID=8b9626b917e59217:T=1506403482:S=ALNI_MbAKcZYY6V99YsmH0kBd3mZ91jclA; _jzqx=1.1506410289.1506414510.2.jzqsr=tripadvisor%2Ecn|jzqct=/attractions-g60763-activities-new_york_city_new_york%2Ehtml.jzqsr=tripadvisor%2Ecn|jzqct=/attraction_review-g60763-d105127-reviews-central_park-new_york_city_new_york%2Ehtml; TAAuth3=3%3A85029581b5ce1f0754f35b089901fc98%3AAEr9FavHiia82os895Avxu0SrGHwZGLD1aBgEid1%2BZvRt%2FkX6UPOyQwWx9dL6Egu%2F9zWR4rYqa6S68p5%2FkUAA74mv1f9qRcDJjeCXu5jIBZrDgyH5MFtvF9opp0ve%2B%2B%2FvTywfw8BMp679ClsGe4hpNmb4J5dpFcXnzLNB78%2BvXhx4ZllSTctETvFygYGsI6ViQ%3D%3D; CommercePopunder=SuppressAll*1506414893809; ServerPool=B; TATravelInfo=V2*A.2*MG.-1*HP.2*FL.3*RVL.60763_269l105127_269*RS.1; CM=%1%HanaPersist%2C%2C-1%7CPremiumMobSess%2C%2C-1%7Ct4b-pc%2C%2C-1%7CHanaSession%2C%2C-1%7CRCPers%2C%2C-1%7CWShadeSeen%2C%2C-1%7CFtrPers%2C%2C-1%7CTheForkMCCPers%2C%2C-1%7CHomeASess%2C1%2C-1%7CPremiumSURPers%2C%2C-1%7CPremiumMCSess%2C%2C-1%7CCpmPopunder_1%2C1%2C1506481452%7CCCSess%2C%2C-1%7CCpmPopunder_2%2C1%2C-1%7CPremRetPers%2C%2C-1%7CViatorMCPers%2C%2C-1%7Csesssticker%2C%2C-1%7C%24%2C%2C-1%7CPremiumORSess%2C%2C-1%7Ct4b-sc%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS2%2C%2C-1%7Cb2bmcpers%2C%2C-1%7CMC_IB_UPSELL_IB_LOGOS%2C%2C-1%7CPremMCBtmSess%2C%2C-1%7CPremiumSURSess%2C%2C-1%7CLaFourchette+Banners%2C%2C-1%7Csess_rev%2C%2C-1%7Csessamex%2C%2C-1%7CPremiumRRSess%2C%2C-1%7CSaveFtrPers%2C%2C-1%7CTheForkORSess%2C%2C-1%7CTheForkRRSess%2C%2C-1%7Cpers_rev%2C%2C-1%7CMetaFtrSess%2C%2C-1%7CRBAPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_PERSISTANT%2C%2C-1%7CFtrSess%2C%2C-1%7CHomeAPers%2C%2C-1%7CPremiumMobPers%2C%2C-1%7CRCSess%2C%2C-1%7CLaFourchette+MC+Banners%2C%2C-1%7Csh%2C%2C-1%7CLastPopunderId%2C137-1859-null%2C-1%7Cpssamex%2C%2C-1%7CTheForkMCCSess%2C%2C-1%7CCCPers%2C%2C-1%7CWAR_RESTAURANT_FOOTER_SESSION%2C%2C-1%7Cb2bmcsess%2C%2C-1%7CPremRetSess%2C%2C-1%7CViatorMCSess%2C%2C-1%7CPremiumMCPers%2C%2C-1%7CPremiumRRPers%2C%2C-1%7CTheForkORPers%2C%2C-1%7CPremMCBtmPers%2C%2C-1%7CTheForkRRPers%2C%2C-1%7CSaveFtrSess%2C%2C-1%7CPremiumORPers%2C%2C-1%7CRBASess%2C%2C-1%7Cperssticker%2C%2C-1%7CCPNC%2C%2C-1%7CMetaFtrPers%2C%2C-1%7C; TAReturnTo=%1%%2FAttraction_Review-g60763-d105127-Reviews-Central_Park-New_York_City_New_York.html; roybatty=TNI1625!ALtGms0D6IUsfQWSBuaSbfDEmZ4ftHPduiv1GymLVK5qBJ%2FNjJID9j4e6nhuXmgk9qzugmpsytimbkDMQMbWZUyjmJ1aGqyYxJ%2Fv5x6j4EEgfnnd5RTGtQIKgu6viobldRO4nV%2FC9bvWIjHfm0oTHYmkJiAZtcasHZtvN27UGYOb%2C1; _ga=GA1.2.1891635985.1506395074; _gid=GA1.2.387104561.1506395074; ki_t=1506395073193%3B1506473900478%3B1506473914258%3B2%3B15; ki_r=; _jzqa=1.3643963285031360000.1506395069.1506414510.1506473899.4; _jzqc=1; Hm_lvt_2947ca2c006be346c7a024ce1ad9c24a=1506395069,1506473898; Hm_lpvt_2947ca2c006be346c7a024ce1ad9c24a=1506473915; _qzja=1.1053412328.1506395069340.1506414509367.1506473898520.1506473898520.1506473916449..0.0.15.4; _qzjb=1.1506473898519.2.0.0.0; _qzjc=1; _qzjto=2.1.0; _jzqb=1.2.10.1506473899.1; TASession=%1%V2ID.92BEF1B35C9E0A42C6529A5842018B7E*SQ.8*LP.%2FLangRedirect%3Fauto%3D3%26origin%3Dzh%26pool%3DB%26returnTo%3D%252FAttractions-g60763-Activities-New_York_City_New_York%5C.html*LS.DemandLoadAjax*GR.44*TCPAR.68*TBR.65*EXEX.49*ABTR.20*PHTB.28*FS.55*CPU.83*HS.recommended*ES.popularity*AS.popularity*DS.5*SAS.popularity*FPS.oldFirst*TS.A86D0BBD5C49EF50548CDD1A204E943F*LF.zhCN*FA.1*DF.0*IR.3*OD.zh*MS.-1*RMS.-1*FLO.60763*TRA.true*LD.105127; TAUD=LA-1506395051802-1*RDD-1-2017_09_25*LG-78873468-2.1.F.*LD-78873469-.....'
}

url_saves = "https://www.tripadvisor.cn/Attraction_Review-g60763-d105127-Reviews-Central_Park-New_York_City_New_York.html"
# 获得请求信息
wb_data = requests.get(url_saves, headers=headers)
soup = BeautifulSoup(wb_data.text, 'lxml')
print(soup)
