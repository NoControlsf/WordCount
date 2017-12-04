import re
import sqlite3 as sqlite
import urllib
import requests
import zlib
from bs4 import BeautifulSoup
# 土地交易信息汇总
def transaction_list():
    page_num = 1
    num_list = []
    for a in range(11):
        num_list.append(a*100 + 1)
    for i in num_list:
        print(i)
        url = "http://www.bjgtj.gov.cn/sjzy/front/project/theTransactionlist/dataproxy.do?startrecord={}&endrecord={}&perpage=20".format(1101, 1198)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'Coolie': 'JSESSIONID=076C698573892B319E210B308B66F6D5; __jsluid=220c773a5a4c7a15e881c279e01a0525; _gscs_661311108=096697114h6i7519|pv:3; _gscbrs_661311108=1; _va_id=22417e2ff2ac0529.1509669715.1.1509670641.1509669715.; _va_ses=*; _gscu_661311108=09669711mgqaye19Host:www.bjgtj.gov.cn'
        }
        wb_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')

        reg = re.compile(r"(?<=\=)\d+")  # 匹配等号后的数字
        detail_num_list = []
        for tr in soup.findAll('tr', class_='datagrid-Item'):
            td_list = tr.findAll('td')
            td_list2 = []
            for td in td_list:
                sth = td.get_text()
                td_list2.append(sth)
                sa = td.find('a', id='e')
                if sa != None:
                    hr = str(sa['href'])
                    numb = reg.search(hr).group(0)
                    td_list2.append(numb)
            print(td_list2[2])
            # sql = 'replace into transactionlist values({})'.format(('?,' * len(td_list2))[:-1])
            # conn = sqlite.connect("E:/stock/fdcstock.db")
            # cur = conn.cursor()
            # cur.execute(sql, td_list2)
            # conn.commit()
            # conn.close()
            detail_num = td_list2[2]
            detail_num_list.append(detail_num)
        for count in detail_num_list:
            transaction_detail(count)

# 宗地明细信息
def transaction_detail(count):
    # detail_url = "http://www.bjgtj.gov.cn/sjzy/front/project/theTransactionlist/result.do?iid={}".format(count)
    detail_url = "http://www.bjgtj.gov.cn/sjzy/front/project/theTransactionlist/result.do?iid={}".format(count)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
        'Coolie': 'JSESSIONID=E49DCA87513554FEB8D5DCE3242D8BFF; __jsluid=220c773a5a4c7a15e881c279e01a0525; _va_id=22417e2ff2ac0529.1509669715.6.1509937920.1509936059.; _va_ses=*; _gscs_661311108=t09936059tgyh0j16|pv:4; _gscbrs_661311108=1; _gscu_661311108=09669711mgqaye19'
    }
    wb_data = requests.get(detail_url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    div = soup.find('div', id='ess_ctr5420_ModuleContent')
    content_list = []
    # print(div)
    iid = count  # iid
    content_list.append(iid)
    title = div.find('span', id='title').get_text()  # 标题
    content_list.append(title)
    publishtime = div.find('span', id='publishtime').get_text()  # 发行时间
    content_list.append(publishtime)
    serialNO = div.find('span', id='serialNO').get_text()  # 交易文件编号
    content_list.append(serialNO)
    usersize = div.find('span', id='usersize').get_text()  # 建设用地面积(平方米)
    content_list.append(usersize)
    agentsize = div.find('span', id='agentsize').get_text()  # 代征地面积(平方米)
    content_list.append(agentsize)
    minplansize1 = div.find('span', id='minplansize')
    if minplansize1 != None:
        minplansize = div.find('span', id='minplansize').get_text()  # 规划建筑面积最小值(平方米)
        content_list.append(minplansize)
    else:
        content_list.append('')
    maxplansize1 = div.find('span', id='maxplansize')
    if maxplansize1 != None:
        reg = re.compile(r"(?<=≤)\d+")  # 匹配符合后的数字
        maxplansize = div.find('span', id='maxplansize').get_text()  # 规划建筑面积最大值(平方米)
        content_list.append(reg.search(maxplansize).group(0))
    else:
        content_list.append('')
    purposedetail = div.find('span', id='purposedetail').get_text()  # 用地性质
    content_list.append(purposedetail)
    devdegree = div.find('span', id='devdegree').get_text()  # 土地开发程度
    content_list.append(devdegree)
    address = div.find('span', id='address').get_text()  # 地块位置
    content_list.append(address)
    auctiontime = div.find('span', id='auctiontime')  # 挂牌竞价起始时间
    if auctiontime != None:
        content_list.append(div.find('span', id='auctiontime').get_text())
    else:
        content_list.append('')
    auctionendtime = div.find('span', id='auctionendtime')  # 投标时间
    if auctionendtime != None:
        content_list.append(div.find('span', id='auctionendtime').get_text())
    else:
        content_list.append('')
    startingprice = div.find('span', id='startingprice')  # 起始价(万元)
    if startingprice != None:
        content_list.append(div.find('span', id='startingprice').get_text())
    else:
        content_list.append('')
    ess_ctr5420_ProjectDetail_lblBuyEndTime = div.find('span', id='ess_ctr5420_ProjectDetail_lblBuyEndTime')  # 挂牌竞买申请截止时间
    if ess_ctr5420_ProjectDetail_lblBuyEndTime != None:
        content_list.append(div.find('span', id='ess_ctr5420_ProjectDetail_lblBuyEndTime').get_text())
    else:
        content_list.append('')
    gdprice = div.find('span', id='gdprice')  # 固定交易价格
    if gdprice != None:
        content_list.append(div.find('span', id='gdprice').get_text())
    else:
        content_list.append('')
    ess_ctr5420_ProjectDetail_lblAuctionEndTime = div.find('span', id='ess_ctr5420_ProjectDetail_lblAuctionEndTime')  # 挂牌竞价截止时间
    if ess_ctr5420_ProjectDetail_lblAuctionEndTime != None:
        content_list.append(div.find('span', id='ess_ctr5420_ProjectDetail_lblAuctionEndTime').get_text())
    else:
        content_list.append('')
    smallestincrement = div.find('span', id='smallestincrement')  # 最小递增幅度(万元)
    if smallestincrement != None:
        content_list.append(div.find('span', id='smallestincrement').get_text())
    else:
        content_list.append('')
    margin1 = div.find('span', id='margin')
    if margin1 != None:
        margin = div.find('span', id='margin').get_text()  # 保证金(万元)
        content_list.append(margin)
    else:
        content_list.append('')
    ess_ctr5420_ProjectDetail_hplOtherFile1 = div.find('a', id='ess_ctr5420_ProjectDetail_hplOtherFile')
    if ess_ctr5420_ProjectDetail_hplOtherFile1 != None:
        ess_ctr5420_ProjectDetail_hplOtherFile = div.find('a', id='ess_ctr5420_ProjectDetail_hplOtherFile').get_text()  # 其它文件下载
        content_list.append(ess_ctr5420_ProjectDetail_hplOtherFile)
    else:
        content_list.append('')
    tradesubpositionid1 = div.find('span', id='tradesubpositionid')
    if tradesubpositionid1 != None:
        tradesubpositionid = div.find('span', id='tradesubpositionid').get_text()  # 交易地点
        content_list.append(tradesubpositionid)
    else:
        content_list.append('')
    contactphone1 = div.find('span', id='contactphone')
    if contactphone1 != None:
        contactphone = div.find('span', id='contactphone').get_text()  # 联系电话
        content_list.append(contactphone)
    else:
        content_list.append('')
    postcontent1 = div.find('a', id='postcontent')
    if postcontent1 != None:
        # 下载文件部分开始
        postcontent = div.find('a', id='postcontent')['href']  # 挂牌交易公告文件
        url = 'http://www.bjgtj.gov.cn/sjzy/front/project/theTransactionlist/download.do'
        headers = {'Host': 'www.bjgtj.gov.cn',
                    'Accept-Encoding': 'gzip, deflate',
                    'Referer': 'http://www.bjgtj.gov.cn/sjzy/front/project/theTransactionlist/result.do?iid={}'.format(count),
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36'}
        regfile = re.compile(r"(?<=\=)\S+")  # 匹配符合后的字符串
        regfileType = re.compile(r"(?<=\.)\S+")  # 匹配符合后的字符串
        fileName = regfile.search(postcontent).group(0)
        fileType = regfileType.search(fileName).group(0)
        values = {'newFileName': fileName}
        postdata = urllib.parse.urlencode(values).encode('utf-8')
        r = urllib.request.Request(url, postdata, headers)
        u = urllib.request.urlopen(r, timeout=15)
        info = u.info()
        if info['Content-Encoding'] == 'gzip':
            doc = zlib.decompress(u.read(), zlib.MAX_WBITS|16)
        elif info['Content-Encoding'] == 'deflate':
            doc = zlib.decompress(u.read(), -zlib.MAX_WBITS)
        if info['Content-Type'] == 'application/octet-stream':
            open('E:\stock\FDCFile\{}'.format(str(count)+'.'+fileType), mode='wb').write(doc)
            content_list.append('E:\stock\FDCFile\{}'.format(str(count)+'.'+fileType))  # 下载文档路径 E:\stock\FDCFile\
        else:
            content_list.append('')  # 下载文档路径
            # raise Exception('Unknown Content-Type:' + info['Content-Type'])
    else:
        content_list.append('')  # 下载文档路径
    # 下载文件部分结束

    HistoryDiv1 = div.find('div', class_='HistoryDiv')
    if HistoryDiv1 != None:
        HistoryDiv = div.find('div', class_='HistoryDiv').get_text()
        HistoryDiv2 = HistoryDiv.replace('\r', '').replace('\t', '').replace('\n', '').replace('\u2003', '')
        content_list.append(HistoryDiv2)  # 历史报价
    else:
        content_list.append('')  # 历史报价
    ess_ctr5420_ProjectDetail_lblTradeTime = div.find('span', id='ess_ctr5420_ProjectDetail_lblTradeTime').get_text()  # 成交时间
    content_list.append(ess_ctr5420_ProjectDetail_lblTradeTime)
    ess_ctr5420_ProjectDetail_lblTradePrice = div.find('span', id='ess_ctr5420_ProjectDetail_lblTradePrice').get_text()  # 成交价格
    content_list.append(ess_ctr5420_ProjectDetail_lblTradePrice.replace('\r', '').replace('\t', '').replace('\n', '').replace(' ', ''))
    ess_ctr5420_ProjectDetail_lblOwner = div.find('span', id='ess_ctr5420_ProjectDetail_lblOwner').get_text()  # 竞得人
    content_list.append(ess_ctr5420_ProjectDetail_lblOwner)
    ess_ctr5420_ProjectDetail_lblother = div.find('span', id='ess_ctr5420_ProjectDetail_lblother').get_text()  # 其他竞得条件
    content_list.append(ess_ctr5420_ProjectDetail_lblother)

    print(content_list)
    sql = 'replace into transactionDetail values({})'.format(('?,' * len(content_list))[:-1])
    conn = sqlite.connect("E:/stock/fdcstock.db")
    cur = conn.cursor()
    cur.execute(sql, content_list)
    conn.commit()
    conn.close()

# 土地出让信息
def  land_leasing_list():
    page_num = 1
    num_list = []
    # for a in range(111):
    for a in range(111):
        num_list.append(a*75 + 1)
    for i in num_list:
        print(i)
        url = 'http://www.bjgtj.gov.cn/sjzy/front/landsold/dataproxy.do?startrecord={}&endrecord={}&perpage=15'.format(i, i+74)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
            'Coolie': 'JSESSIONID=6CA4148F8EFD69BBCA981DB76373F0E6; __jsluid=220c773a5a4c7a15e881c279e01a0525; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1510020596; Hm_lpvt_d7682ab43891c68a00de46e9ce5b76aa=1510020653; _gscs_661311108=t10027233rord2d10|pv:23; _gscbrs_661311108=1; _gscu_661311108=09669711mgqaye19; _va_id=22417e2ff2ac0529.1509669715.13.1510034881.1510027234.; _va_ses=*'
        }
        wb_data = requests.get(url, headers=headers)
        soup = BeautifulSoup(wb_data.text, 'lxml')
        reg = re.compile(r"(?<=\=)\d+")  # 匹配等号后的数字
        detail_num_list = []
        for tr in soup.findAll('tr'):
            td_list = tr.findAll('td')
            td_list2 = []
            for td in td_list:
                sth = td.get_text()
                td_list2.append(sth)
                sa = td.find('a')
                if sa != None:
                    hr = str(sa['href'])
                    numb = reg.search(hr).group(0)
                    td_list2.pop()
                    td_list2.append(numb)
            print(td_list2)
            sql = 'replace into landLeasingList values({})'.format(('?,' * len(td_list2))[:-1])
            conn = sqlite.connect("E:/stock/fdcstock.db")
            cur = conn.cursor()
            cur.execute(sql, td_list2)
            conn.commit()
            conn.close()
            detail_num = td_list2[3]
            detail_num_list.append(detail_num)
        print(detail_num_list)
        for count in detail_num_list:
            leasing_detail(count)
# 土地出让结果
def leasing_detail(count):
    detail_url = "http://www.bjgtj.gov.cn/sjzy/front/landsold/oprcadastral.do?iid={}".format(count)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3195.0 Safari/537.36',
        'Coolie': 'JSESSIONID=A2B4951862C927F503E24C8577A8468B; __jsluid=220c773a5a4c7a15e881c279e01a0525; Hm_lvt_d7682ab43891c68a00de46e9ce5b76aa=1510020596; Hm_lpvt_d7682ab43891c68a00de46e9ce5b76aa=1510020653; _gscbrs_661311108=1; _gscu_661311108=09669711mgqaye19; _va_id=22417e2ff2ac0529.1509669715.13.1510034881.1510027234.'
    }
    wb_data = requests.get(detail_url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    content_list = []
    iid = count  # iid
    content_list.append(iid)
    ess_ctr7856_LandSoldView_lblReceiveName1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblReceiveName')
    if ess_ctr7856_LandSoldView_lblReceiveName1 != None:
        ess_ctr7856_LandSoldView_lblReceiveName = soup.find('span', id='ess_ctr7856_LandSoldView_lblReceiveName').get_text()  # 受让方名称
        content_list.append(ess_ctr7856_LandSoldView_lblReceiveName)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblLandPosition1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandPosition')
    if ess_ctr7856_LandSoldView_lblLandPosition1 != None:
        ess_ctr7856_LandSoldView_lblLandPosition = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandPosition').get_text()  # 土地位置
        content_list.append(ess_ctr7856_LandSoldView_lblLandPosition)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblLandCountry1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandCountry')
    if ess_ctr7856_LandSoldView_lblLandCountry1 != None:
        ess_ctr7856_LandSoldView_lblLandCountry = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandCountry').get_text()  # 区县
        content_list.append(ess_ctr7856_LandSoldView_lblLandCountry)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblLandArea1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandArea')
    if ess_ctr7856_LandSoldView_lblLandArea1 != None:
        ess_ctr7856_LandSoldView_lblLandArea = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandArea').get_text()  # 宗地面积
        content_list.append(ess_ctr7856_LandSoldView_lblLandArea.replace('\r', '').replace('\n', '').replace(' ', ''))
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblBuildArea1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblBuildArea')
    if ess_ctr7856_LandSoldView_lblBuildArea1 != None:
        ess_ctr7856_LandSoldView_lblBuildArea = soup.find('span', id='ess_ctr7856_LandSoldView_lblBuildArea').get_text()  # 规划建筑面积
        content_list.append(ess_ctr7856_LandSoldView_lblBuildArea)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblLandUseFul1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandUseFul')
    if ess_ctr7856_LandSoldView_lblLandUseFul1 != None:
        ess_ctr7856_LandSoldView_lblLandUseFul = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandUseFul').get_text()  # 规划用途
        content_list.append(ess_ctr7856_LandSoldView_lblLandUseFul)
    else:
        content_list.append('')
    ess_ctr7856_LandsoldView_lblLandPrice1 = soup.find('span', id='ess_ctr7856_LandsoldView_lblLandPrice')
    if ess_ctr7856_LandsoldView_lblLandPrice1 != None:
        ess_ctr7856_LandsoldView_lblLandPrice = soup.find('span', id='ess_ctr7856_LandsoldView_lblLandPrice').get_text()  # 土地成交价
        content_list.append(ess_ctr7856_LandsoldView_lblLandPrice)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblLandBound1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandBound')
    if ess_ctr7856_LandSoldView_lblLandBound1 != None:
        ess_ctr7856_LandSoldView_lblLandBound = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandBound').get_text()  # 宗地四至
        content_list.append(ess_ctr7856_LandSoldView_lblLandBound)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblLandGData1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandGData')
    if ess_ctr7856_LandSoldView_lblLandGData1 != None:
        ess_ctr7856_LandSoldView_lblLandGData = soup.find('span', id='ess_ctr7856_LandSoldView_lblLandGData').get_text()  # 签约时间
        content_list.append(ess_ctr7856_LandSoldView_lblLandGData)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblFaithSTime1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblFaithSTime')
    if ess_ctr7856_LandSoldView_lblFaithSTime1 != None:
        ess_ctr7856_LandSoldView_lblFaithSTime = soup.find('span', id='ess_ctr7856_LandSoldView_lblFaithSTime').get_text()  # 合同约定开工时间
        content_list.append(ess_ctr7856_LandSoldView_lblFaithSTime)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblFaithETime1 = soup.find('span', id='ess_ctr7856_LandSoldView_lblFaithETime')
    if ess_ctr7856_LandSoldView_lblFaithETime1 != None:
        ess_ctr7856_LandSoldView_lblFaithETime = soup.find('span', id='ess_ctr7856_LandSoldView_lblFaithETime').get_text()  # 合同约定竣工时间
        content_list.append(ess_ctr7856_LandSoldView_lblFaithETime)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblcubagerate1 =soup.find('span', id='ess_ctr7856_LandSoldView_lblcubagerate')
    if ess_ctr7856_LandSoldView_lblcubagerate1 != None:
        ess_ctr7856_LandSoldView_lblcubagerate = soup.find('span', id='ess_ctr7856_LandSoldView_lblcubagerate').get_text()  # 容积率（地上）
        content_list.append(ess_ctr7856_LandSoldView_lblcubagerate)
    else:
        content_list.append('')
    ess_ctr7856_LandSoldView_lblsignupdate1 =soup.find('span', id='ess_ctr7856_LandSoldView_lblsignupdate')
    if ess_ctr7856_LandSoldView_lblsignupdate1 != None:
        ess_ctr7856_LandSoldView_lblsignupdate = soup.find('span', id='ess_ctr7856_LandSoldView_lblsignupdate').get_text()  # 发布时间
        content_list.append(ess_ctr7856_LandSoldView_lblsignupdate)
    else:
        content_list.append('')
    print(content_list)
    sql = 'replace into landLeasingDetail values({})'.format(('?,' * len(content_list))[:-1])
    conn = sqlite.connect("E:/stock/fdcstock.db")
    cur = conn.cursor()
    cur.execute(sql, content_list)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    # transaction_list()
    # transaction_detail(2300)
    land_leasing_list()
    # leasing_detail(4607)