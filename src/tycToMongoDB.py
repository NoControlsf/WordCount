# -*- coding: utf-8 -*-
"""
Created on 17-7-18

@author: hy_qiu
"""
import json
import multiprocessing.dummy as mt
import os
import re
import time
from pymongo import MongoClient
import pymysql
import requests

import util.excel
import util.fileutil
import util.js
import util.mt
import util.verify
from bs4 import BeautifulSoup
from util.wraps import retry

import src.util.loginit
import os.path
AGENT_FIREFOX = 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'
# AGENT_Android7 = 'Mozilla/5.0 (Linux; U; Android 7.0; zh-cn;)'
TYC_HOST = 'https://www.tianyancha.com'

SOGOU = [
    '6b-f2--5-----ec---98-------034d1a-7--',
    '18-------b9fd7-c--203-------46-a-5e--',
    '-6-0--3----d-ea---f43b-7-c-8-219----5',
    '-70d--ac----f6-e-4b5--9-----3----21-8',
    '--3-1--45-c-7--2-a-e--b-8-6--0d----f9',
    '----3d658----b4------a01c9-27-e---f--',
    '8---d-7--4-f---2e9--5-1---63--b--ca-0',
    'd49---5---c-6b----a-3------207--8f1-e',
    '7---65-------0-----f--9--12-4e8cbad-3',
    '1-8--fl52--9----e-d4-b-a-c--3--0--7-6']

BREAK_EVENT = mt.Event()
_LOCK = mt.Lock()
_DONE = mt.Value('i', 0)
_FAIL = mt.Value('i', 0)
_EMPTY = mt.Value('i', 0)

logger = src.util.loginit.get_logger('tyc2')


def get_login():
    url = 'https://www.tianyancha.com/cd/login.json'

    login_json = {'mobile': '13606181270',
                  'cdpassword': 'de2acaac3f5037d6acfba46454cbca87',
                  'loginway': 'PL',
                  'autoLogin': True}
    """
    login_json = {'mobile': '18361296750',
                  'cdpassword': '8dd8734a6c52f4303dd36cc61e11b6fc',
                  'loginway': 'PL',
                  'autoLogin': True}
    """

    resp = SESS.post(url, json=login_json)
    logger.info('get login')
    resp.raise_for_status()
    data = resp.json()
    print(data['state'])
    if data['state'] == 'ok':
        SESS.cookies.set('auth_token', data['data']['token'])
        SESS.cookies.set('tyc-user-info', util.js.encodeURIComponent(data['data']))
    return True


SESS = requests.session()
SESS.headers['User-Agent'] = AGENT_FIREFOX
get_login()


def wait_for_verify():
    logger.warning('wait_for_verify start')
    while not util.verify.chk_TYC(SESS):
        if BREAK_EVENT.is_set():
            return
        time.sleep(1)
    logger.warning('wait_for_verify OK')
    time.sleep(1)


def get_utm(key, utm_chars):
    asc = ord(str(key)[0])
    idx = (int(str(asc)[1]) + 1) % 10
    utm = ''.join([SOGOU[idx][int(c)] for c in utm_chars])
    return utm


# 页面分析 PageFunction 默认处理函数 取其中的Table 返回json
def pgf_table(datainfo, div_head):
    tb = div_head.find('table', class_='companyInfo-table')
    if len(datainfo.colnames) == 0:
        for th in tb.thead.find_all('th'):
            datainfo.colnames.append(th.get_text(strip=True))
        datainfo.formatcolumn()
    for tr in tb.tbody.find_all('tr'):
        tds = list(tr.find_all('td'))
        # print(tds)
        item = {}
        for i in range(len(datainfo.colnames)):
            key = datainfo.colnames[i]
            if key == '':
                continue
            elif datainfo.cdfdict and key in datainfo.cdfdict.keys():
                item[key] = cdf_text(tds[i], datainfo.cdfdict[key])
            else:
                item[key] = tds[i].get_text(strip=True)
        yield item


# 字段分析 ColumnDefineFunction 默认处理函数
# cdf :string  表示element.find(cdf).getText
# cdf :callable  表示cdf(element)
# cdf :'' or None  表示忽略
def cdf_text(element, cdf=None):
    if cdf is None or cdf == '':
        return
    elif isinstance(cdf, str):
        tag = element.find(cdf)
        if tag:
            return tag.get_text(strip=True)
    elif callable(cdf):
        return cdf(element)
    else:
        return element.get_text(strip=True)


# 字段分析 ColumnDefineFunction “详情”
"""
def cdf_more(element):
    span = element.find('span', class_='companyinfo_show_more_btn')
    if span and span.has_attr('onclick'):
        jsonstr = re.findall('\w+\((.+)\)', span['onclick'])
        if jsonstr and len(jsonstr):
            try:
                # pattern = re.compile('"(.*)"')
                # print(pattern.findall(jsonstr[0]))
                return json.loads(jsonstr[0])
            except:
                pass
    return ''
"""
def cdf_more(element):
    span = element.find('script')
    # print(span.get_text())
    return json.loads(span.get_text())


# 字段分析 ColumnDefineFunction 对外投资企业的年报信息
def cdf_invest(element):
    a = element.find('a')
    if a:
        compid = a['href'].split('/')[-1].strip()
        compna = '对外投资-' + a.get_text(strip=True)
        return TYC2(compna, compid).get_company([DataInfo_Report])
    else:
        return element.get_text(strip=True)


# AnnouncementOfWinningTheBid 中标公告
def wtb_announcement(element):
    a = element.find('a')
    url = 'https://www.tianyancha.com%s' % a['href']
    # print(url)
    wb_data = SESS.get(url, params=None, timeout=60)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    div = soup.find('div', class_='common-remark-style')
    link = div.find('a')
    link_h = link['href']
    title = a.get_text()
    dic = {'标题': title, '原始链接': link_h}
    return dic


def get_base(soup):
    base = {}

    div = soup.find('div', class_='company_header_width')

    base['名称'] = div.div.span.get_text(strip=True)

    div_row = list(div.find_all('div', recursive=False))

    div_col = list(div_row[1].find_all('div'))

    base['电话'] = list(div_col[1].find_all('span'))[1].get_text(strip=True)

    base['邮箱'] = list(div_col[1].find_all('span'))[4].get_text(strip=True)

    div_col = list(div_row[1].find_all('div'))

    web = div_row[1].find('a')
    base['网址'] = web.get_text(strip=True) if web else ''

    base['地址'] = list(div_col[4].find_all('span'))[3].get_text(strip=True)


    # div_row = list(div.find_all('div', class_='sec-c2', recursive=False))  # 有些没有简介
    # div_col = list(div_row[0].find_all('span'))
    # base['简介'] = div_col[0].get_text(strip=True).split('：')[1:]  # 截取‘简介：’后面的数据

    div = soup.find('div', class_='baseInfo_model2017')
    tb = div.find('table', class_='companyInfo-table').tbody
    tds = list(tb.find_all('td'))
    a = tds[0].find('a', title=True)
    base['法人'] = a.get_text(strip=True) if a else ''
    div_col = tds[1].find_all('div', class_='baseinfo-module-content-value')
    base['注册资本'] = div_col[0].get_text(strip=True)
    base['注册时间'] = div_col[1].get_text(strip=True)
    base['企业状态'] = div_col[2].get_text(strip=True)

    div = soup.find('div', class_='base0910')
    tdList = []
    for td in div.find_all('td'):
        tdList.append(td.contents[0])
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    base[tdList[0]] = tdList[1]
    base[tdList[2]] = tdList[3]
    base[tdList[5]] = tdList[6]
    base[tdList[7]] = tdList[8]
    base[tdList[9]] = tdList[10]
    base[tdList[11]] = tdList[12]
    base[tdList[13]] = re_h.sub('', str(tdList[14]))  # 去掉HTML 标签
    base[tdList[15]] = re_h.sub('', str(tdList[16]))  # 去掉HTML 标签
    base[tdList[17]] = tdList[18]
    base[tdList[19]] = tdList[20]
    base[tdList[21]] = tdList[22]
    base[tdList[23]] = re_h.sub('', str(tdList[24]))  # 去掉HTML 标签
    """
    base['名称'] = '中国电力国际发展有限公司'
    base['电话'] = ''
    base['邮箱'] = ''
    base['网址'] = ''
    base['地址'] = ''
    base['法人'] = ''
    base['注册资本'] = ''
    base['注册时间'] = '2004-03-24'
    base['企业状态'] = '仍注册'
    base['工商注册号'] = ''
    base['组织机构代码'] = ''
    base['统一信用代码'] = ''
    base['公司类型'] = '公众股份有限公司'
    base['纳税人识别号'] = ''
    base['行业'] = ''
    base['营业期限'] = ''
    base['核准日期'] = ''
    base['登记机关'] = ''
    base['英文名称'] = 'CHINA POWER INTERNATIONAL DEVELOPMENT LIMITED'
    base['注册地址'] = ''
    base['经营范围'] = ''
    """
    return base


# 页面分析 PageFunction 主要人员
def pfg_staff(di, div_head):
    for div in div_head.find_all('div', class_='staffinfo-module-container'):
        title = div.div.div.get_text(strip=True)
        tname = div.div.a.get_text(strip=True)
        yield {'姓名': tname, '职位': title}


# 页面分析 PageFunction 企业简介
def pgf_stockbrife(di, div_head):
    brife = {}
    tb = div_head.find('table', class_='companyInfo-table')
    for tr in tb.find_all('tr'):
        tds = list(tr.find_all('td'))
        for i in range(len(tds)):
            if tds[i].has_attr('class') and 'table-left' in tds[i]['class']:
                key = tds[i].get_text(strip=True)
                brife[key] = tds[i + 1].get_text(strip=True)
    yield brife


# 页面分析 PageFunction 核心团队
def pgf_teamMember(di, div_head):
    for div in div_head.find_all('div', class_='team-item'):
        name = div.find('div', class_='team-name').get_text(strip=True)
        title = div.find('div', class_='team-title').get_text(strip=True)
        brife = div.find('ul').get_text(strip=True)
        yield {'姓名': name, '职位': title, '简介': brife}


# 页面分析 PageFunction 企业业务
def pgf_firmProduct(di, div_head):
    for div in div_head.find_all('div', class_='product-item'):
        title = div.find('span', class_='title').get_text(strip=True)
        hangye = div.find('div', class_='hangye').get_text(strip=True)
        yeweu = div.find('div', class_='yeweu').get_text(strip=True)
        yield {'名称': title, '类型': hangye, '简介': yeweu}


class DataInfo:
    _datalist = {'seniorPeople': {'ps': 10, 'searchParam': 'id'},
                 'holdingCompany': {'ps': 10, 'searchParam': 'id'},
                 'announcement': {'ps': 10, 'searchParam': 'id'},
                 'equityChange': {'ps': 10, 'searchParam': 'id'},
                 'bonus': {'ps': 10, 'searchParam': 'id'},
                 'staff': {'ps': 20, 'searchParam': 'id'},
                 'holder': {'ps': 20, 'searchParam': 'id'},
                 'invest': {'ps': 20, 'searchParam': 'id'},
                 'changeinfo': {'ps': 5, 'searchParam': 'id'},
                 'branch': {'ps': 10, 'searchParam': 'id'},
                 'touzi': {'ps': 10, 'searchParam': 'name'},
                 'rongzi': {'ps': 10, 'searchParam': 'name'},
                 'teamMember': {'ps': 5, 'searchParam': 'name'},
                 'firmProduct': {'ps': 15, 'searchParam': 'name'},
                 'jingpin': {'ps': 10, 'searchParam': 'name'},
                 'lawsuit': {'ps': 10, 'searchParam': 'name'},
                 'court': {'ps': 5, 'searchParam': 'name'},
                 'zhixing': {'ps': 5, 'searchParam': 'id'},
                 'abnormal': {'ps': 5, 'searchParam': 'id'},
                 'punish': {'ps': 5, 'searchParam': 'name'},
                 'illegal': {'ps': 5, 'searchParam': 'name'},
                 'equity': {'ps': 5, 'searchParam': 'name'},
                 'mortgage': {'ps': 5, 'searchParam': 'name'},
                 'towntax': {'ps': 5, 'searchParam': 'id'},
                 'bid': {'ps': 10, 'searchParam': 'id'},
                 'bond': {'ps': 5, 'searchParam': 'name'},
                 'purchaseland': {'ps': 5, 'searchParam': 'name'},
                 'recruit': {'ps': 10, 'searchParam': 'name'},
                 'taxcredit': {'ps': 5, 'searchParam': 'id'},
                 'check': {'ps': 5, 'searchParam': 'name'},
                 'qualification': {'ps': 5, 'searchParam': 'id'},
                 'product': {'ps': 5, 'searchParam': 'id'},
                 'tmInfo': {'ps': 5, 'searchParam': 'id'},
                 'patent': {'ps': 5, 'searchParam': 'id'},
                 'copyright': {'ps': 5, 'searchParam': 'id'},
                 'icp': {'ps': 5, 'searchParam': 'id'}
                 }

    def __init__(self, name, key, cdfdict=None, coldict=None, pgf=None, headdict=None):
        # cdfdict(column define function): dict { 列名称 : '' (忽略此列) 或 指定tag 或 自定义列操作函数}
        # coldict: {column index or column name:column name}
        # pgf(page function): function(datainfo,div_head) 用户自定义页面解析函数
        self.name = name
        self.key = key
        if headdict:
            self.headdict = headdict
        else:
            self.headdict = {'id': '_container_' + key}

        try:
            self.pageszie = self._datalist[key]['ps']
            self.searchby = self._datalist[key]['searchParam']
        except:
            pass
        self.url = '{}/pagination/{}.xhtml'.format(TYC_HOST, key)
        self.cdfdict = cdfdict
        self.coldict = coldict
        self.colnames = []  # table.thead.th
        if pgf:
            self.pgf = pgf
        else:
            self.pgf = pgf_table

    def formatcolumn(self):
        if not isinstance(self.coldict, dict):
            return
        for k in self.coldict.keys():
            if isinstance(k, int):
                self.colnames[k] = self.coldict[k]
            elif isinstance(k, str):
                for i in range(len(self.colnames)):
                    if self.colnames[i] == k:
                        self.colnames[i] = self.coldict[k]
                        break


DataInfo_Report = DataInfo('企业年报', 'report', headdict={'tyc-event-ch': 'CompangyDetail.nianbao'})

TYC_DATALIST = [
    # 股票信息
    DataInfo('企业简介', 'stockbrife', pgf=pgf_stockbrife, headdict={'id': 'nav-main-stockNum'}),
    DataInfo('高管信息', 'seniorPeople', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    DataInfo('参股控股', 'holdingCompany'),
    DataInfo('股本变动', 'equityChange'),
    DataInfo('分红情况', 'bonus'),

    # 企业背景
    DataInfo('主要人员', 'staff', pgf=pfg_staff),
    DataInfo('股东信息', 'holder', cdfdict={'股东': 'a', '认缴出资': 'span'}, coldict={0: '股东'}),
    DataInfo('对外投资', 'invest', cdfdict={'被投资企业名称': cdf_invest, '被投资法定代表人': 'a'}),
    #DataInfo('对外投资', 'invest', cdfdict={'被投资企业名称': 'span', '被投资法定代表人': 'a'}),

    DataInfo('变更记录', 'changeinfo'),
    DataInfo_Report,  # 企业年报
    DataInfo('分支机构', 'branch'),

    # 企业发展
    DataInfo('融资历史', 'rongzi'),
    DataInfo('核心团队', 'teamMember', pgf=pgf_teamMember),
    DataInfo('企业业务', 'firmProduct', pgf=pgf_firmProduct),
    DataInfo('投资事件', 'touzi'),
    # 竞品信息缺

    # 司法风险
    DataInfo('法律诉讼', 'lawsuit'),
    DataInfo('法院公告', 'court', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    #DataInfo('失信人', 'shixinren', cdfdict={'详情': cdf_more}, coldict={-1: '详情'},
    #         headdict={'tyc-event-ch': 'CompangyDetail.shixinren'}),
    DataInfo('被执行人', 'zhixing'),
    # 开庭公告缺

    # 经营风险
    DataInfo('经营异常', 'abnormal'),
    #DataInfo('行政处罚', 'punish', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    # 严重违法缺
    DataInfo('股权出质', 'equity', cdfdict={'操作': cdf_more}, coldict={-1: '操作'}),
    DataInfo('动产抵押', 'mortgage', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    DataInfo('欠税公告', 'towntax'),
    # 司法拍卖缺

    # 经营状况
    DataInfo('招投标', 'bid', cdfdict={'中标公告': wtb_announcement}, coldict={1: '中标公告'}),
    DataInfo('债券信息', 'bond', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    DataInfo('购地信息', 'purchaseland', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    DataInfo('招聘信息', 'recruit', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    DataInfo('税务评级', 'taxcredit'),
    DataInfo('抽查检查', 'check'),
    #DataInfo('产品信息', 'product', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    # 进出口信用缺
    # 资质证书缺
    # 微信公众号缺

    # 知识产权
    #DataInfo('商标信息', 'tmInfo', coldict={'商标': ''}),
    #DataInfo('专利信息', 'patent'),
    DataInfo('著作权', 'copyright', cdfdict={'详情': cdf_more}, coldict={-1: '详情'}),
    DataInfo('网站备案', 'icp')
]


class TYC2:
    def __init__(self, cname, cid=0):
        if cid == 0:
            cid = self.get_companyid(cname)
        if cid:
            self.cid = cid
            self.cname = cname
        else:
            raise Exception('名称不匹配')

    @retry()
    def get_response(self, url, param=None):
        with _LOCK:
            resp = SESS.get(url, params=param, timeout=60)
            # if resp.url.startswith(TYC_HOST + '/login?'):
            #     while not self.get_login():
            #         time.sleep(2)
            #     resp = SESS.get(url, params=param, timeout=60)
            # el
            if resp.status_code in [401, 403, 503] \
                    or resp.url.find('/antirobot.tianyancha.com/captcha/verify?') >= 0:
                logger.debug('{} {}'.format(resp.status_code, resp.url))
                wait_for_verify()
                resp = SESS.get(url, params=param, timeout=60)

            resp.raise_for_status()
            return resp

    def get_soup(self, url, param=None):
        resp = self.get_response(url, param)
        soup = BeautifulSoup(resp.text, 'html5lib')
        return soup

    @retry()
    def set_cookie(self, key):
        # 取得token 和 utm_chars
        url = '{}/tongji/{}.json'.format(TYC_HOST, key)
        resp = self.get_response(url, {'_': int(time.time() * 1000)})
        try:
            tongji_json = resp.json()
            tongji_data = tongji_json['data'].split(',')
            js_code = ''.join([chr(int(code)) for code in tongji_data])
            token = re.findall('token=(\w+);', js_code)[0]
            utm_chars = re.findall('\'([\d,]+)\'', js_code)[0].split(',')
            utm = get_utm(key, utm_chars)

            SESS.cookies.set('token', token)
            SESS.cookies.set('_utm', utm)
        except Exception as e:
            raise e

    def get_report_detail(self, href):
        report = {}
        soup = self.get_soup(TYC_HOST + href)
        # print(soup)
        div_body = soup.find('div', class_='report_body')
        div_content = list(div_body.find_all('div', recursive=False))[1]
        for div in list(div_content.find_all('div', class_=True)):
            title = div.find('div', class_='report_title')
            tb = div.find('table', class_='table')
            if title is None or tb is None:
                continue
            rpt_key = title.get_text(strip=True)
            thead = tb.find('thead')
            if thead:
                keys = []
                rows = []
                for th in thead.find_all('th'):
                    keys.append(th.get_text(strip=True))

                for tr in tb.tbody.find_all('tr'):
                    tds = list(tr.find_all('td'))
                    row = {}
                    for i in range(len(keys)):
                        row[keys[i]] = tds[i].get_text(strip=True)
                    rows.append(row)
                if len(rows):
                    report[rpt_key] = rows
            else:
                tds = list(tb.find_all('td'))
                item = {}
                for i in range(len(tds)):
                    if tds[i].has_attr('class') and 'report_key' in tds[i]['class']:
                        key = tds[i].get_text(strip=True)
                        item[key] = tds[i + 1].get_text(strip=True)
                report[rpt_key] = item
        return report

    def get_report(self, div_head):
        report = []
        if div_head:
            for rpt in div_head.find_all('a', class_='report_item_2017'):
                year = rpt.get_text(strip=True)
                href = rpt['href']
                d = self.get_report_detail(href)
                if d:
                    d['年度'] = year
                    report.append(d)
        report_str = str(report)
        newstr = report_str.replace('企业经营状态经营状态：经营状态包含营业、停业（歇业）、筹建、关闭、破产等类型。详情>* 名词解释由天眼查合作伙伴北大法宝提供', '企业经营状态').replace('所有者权益合计所有者权益合计：所有者权益是指企业资产扣除负债后由所有者享有的剩余权益。公司的所有者权益又称为股东权...详情>* 名词解释由天眼查合作伙伴北大法宝提供', '所有者权益合计')
        report1 = eval(newstr)
        return report1

    def get_data(self, soup, datainfo):
        data = []
        pageno = 1
        totalpage = 0

        div_head = soup.find('div', datainfo.headdict)
        while div_head:
            if BREAK_EVENT.is_set():
                return
            for item in datainfo.pgf(datainfo, div_head):
                data.append(item)

            pager = div_head.find('div', class_='company_pager')
            if pager:
                totalpage = int(pager.find('div', class_='total').get_text(strip=True)[1:-1])
            pageno += 1
            if pageno > totalpage:
                break
            if datainfo.searchby == 'id':
                self.set_cookie(self.cid)
                param = {'ps': datainfo.pageszie, 'pn': pageno, 'id': self.cid, '_': int(time.time() * 1000)}
            else:
                self.set_cookie(self.cname)
                param = {'ps': datainfo.pageszie, 'pn': pageno, 'name': self.cname, '_': int(time.time() * 1000)}

            div_head = self.get_soup(datainfo.url, param)

        return data

    def get_company(self, datalist=None):
        url = '{}/company/{}'.format(TYC_HOST, self.cid)
        soup = self.get_soup(url)

        comyany = dict()
        comyany['id'] = str(self.cid)

        comyany['基本信息'] = get_base(soup)


        if datalist is None:
            datalist = TYC_DATALIST
        for ti in datalist:
            if BREAK_EVENT.is_set():
                return
            if ti.key == 'report':
                data = self.get_report(soup.find('div', ti.headdict))
            else:
                print(ti.key)
                data = self.get_data(soup, ti)
            if data and len(data):
                comyany[ti.name] = data
                logger.info('{} {} {}'.format(self.cname, ti.name, len(data)))

        return comyany

    def get_companyid(self, cname):
        url = '{}/search'.format(TYC_HOST)
        soup = self.get_soup(url, {'key': cname})
        div_list = soup.find('div', class_='search_result_container')
        if div_list:
            for div in div_list.find_all('div', class_='search_result_single'):
                a = div.find('a', {'tyc-event-ch': 'CompanySearch.Company'})
                if a and cname == a.get_text(strip=True):
                    cid = a['href'].split('/')[-1]
                    return cid


def save_company(no, name, fn):
    try:
        c = TYC2(name).get_company()

        conn = MongoClient('localhost', 27017)
        db = conn.tycdb  # 连接tycdb数据库，没有则自动创建
        my_set = db.beijing_ningxia  # 使用test_set集合，没有则自动创建
        my_set.insert(c)
        print('ok')
        #print(c['id'])
        #成功爬取，ISGET设为1
        mysql_mark(name, 1)
        #成功爬取，添加companyid
        mysql_setid(name, c['id'])
    except Exception as e:
        with _LOCK:
            _FAIL.value += 1
        logger.error('{} {} FAIL {}'.format(no, name, e))
        #爬取失败，ISGET设为2
        mysql_mark(name, 2)

def main(fn, startrow, namecol, pathcol=None, sheetindex=0, poolsize=10):
    if not os.path.exists(fn):
        print('{} dose not exists')
        return
    basepath = os.path.splitext(fn)[0]
    if not os.path.exists(basepath):
        os.mkdir(basepath)

    exists = 0
    total = 0
    results = []
    pool = mt.Pool(poolsize)
    util.mt.allow_break(BREAK_EVENT)
    for no, row in util.excel.read_excel(fn, sheetindex=sheetindex, startrow=startrow):
        name = row[namecol].value.strip()
        if name == '':
            continue
        if pathcol:
            path = row[pathcol].value.strip()
            path = os.path.join(basepath, path)
        else:
            path = basepath

        jfn = os.path.join(path, name + '.json')

        total += 1
        if os.path.exists(jfn):
            exists += 1
        else:
            results.append(pool.apply_async(save_company, (no, name, jfn)))

    logger.info('total:{} exists:{} need to download:{}'.format(total, exists, len(results)))
    if len(results) == 0:
        return

    while True:
        if BREAK_EVENT.is_set():
            pool.terminate()
            pool.join()
            break
        else:
            running = False
            for a in results:
                if not a.ready():
                    running = True
                    break
            if not running:
                break
        BREAK_EVENT.wait(1)
    with _LOCK:
        logger.info('done:{} fail:{} '.format(_DONE.value, _FAIL.value))

#对外投资企业爬取
def openFile(filepath1):
    result_list = []
    filepath = filepath1 + '对外投资.json'
    if os.path.getsize(filepath):
        with open(filepath, 'r', encoding='utf8') as load_f:
            load_dict = json.load(load_f)
            for i in range(len(load_dict)):
                result_list.append(load_dict[i]['被投资公司名称'])
    list = traversalDir_FirstDir(filepath1)
    for tmp in list:
        result_list.remove(tmp)
    return result_list


#定义一个函数，path为你的路径
def traversalDir_FirstDir(path):
    #定义一个列表，用来存储结果
    list = []
    #判断路径是否存在
    if (os.path.exists(path)):
        #获取该目录下的所有文件或文件夹目录
        files = os.listdir(path)
        for file in files:
            #得到该文件下所有目录的路径
            m = os.path.join(path, file)
            #判断该路径下是否是文件夹
            if (os.path.isdir(m)):
                h = os.path.split(m)
                # print(h[1])
                list.append(h[1])
        return list

#查询未爬取的企业
def mysql_search_companys():
    conn = pymysql.connect(
        host='192.168.16.231',
        port=3306,
        user='bigdata',
        passwd='bigdata',
        db='bigdata',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "SELECT NSRMC FROM dj_nsrxx  where char_length(NSRMC) >= 4 AND ISGET is null LIMIT 500 ;"
    cur.execute(sql)
    search_list = []
    for r in cur:
        search_list.append(r['NSRMC'])
    conn.commit()
    conn.close()
    return search_list

#将爬取的企业打标
def mysql_mark(NSRMC, ISGET):
    conn = pymysql.connect(
        host='192.168.16.231',
        port=3306,
        user='bigdata',
        passwd='bigdata',
        db='bigdata',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "UPDATE dj_nsrxx SET ISGET = {} where NSRMC = '{}'".format(ISGET, NSRMC)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

#将爬到的企业添加公司id
def mysql_setid(NSRMC, companyid):
    conn = pymysql.connect(
        host='192.168.16.231',
        port=3306,
        user='bigdata',
        passwd='bigdata',
        db='bigdata',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    sql = "UPDATE dj_nsrxx SET companyid = '{}' where NSRMC = '{}'".format(companyid, NSRMC)
    cur.execute(sql)
    cur.close()
    conn.commit()
    conn.close()

if __name__ == '__main__':
    # main('e:/tyc2/17户集团成员名单汇总.xls', 2, 1, 5, 1)
    # main('d:/用户目录/我的文档/税软/2017/产品/大数据/厦门/总局“523”专案-厦门涉案企业名单.xlsx'
    #      , 3, 2, poolsize=1)

    #companys = openFile('f:/tyc/表2/中信信托有限责任公司/')
    #companys = ['北大方正集团有限公司']
    companys = mysql_search_companys()
    for n in companys:
        # save_company('', n, 'e:/tyc2/北京西城区/' + n + '.json')
        save_company('', n, 'f:/tyc/' + n + '/')
        time.sleep(10)


