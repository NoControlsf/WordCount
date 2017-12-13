import datetime
import time

def dateRange(startDate, ClosingDate):
    # startDate = input("请输入你要查看数据的开始日期：")
    startDate = '2014.1.1'
    # ClosingDate = input("请输入你要查看数据的截止日期：")
    ClosingDate = '2017.12.11'
    #系统自动获取时间
    #localtime = time.localtime(time.time())
    #ClosingDate = str(localtime.tm_year)+"."+str(localtime.tm_mon)+"."+str(localtime.tm_mday)
    #print("截止时间默认为系统当前时间:" + ClosingDate)

    dates = []
    dt = datetime.datetime.strptime(startDate, "%Y.%m.%d")
    date = startDate[:]

    while date <= ClosingDate:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime("%Y.%m.%d")
    return dates
