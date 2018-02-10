import pymysql
import time


def read_sql():
    rfile = open('D:\\qy\\test.sql', 'r', encoding='UTF-8')
    sqlList = []
    sql = ''
    for line in rfile:
        sql += line
        if line.endswith(';'):
            sqlList.append(sql)
            sql = ''
    rfile.close()
    sql_1000_list = []
    sql_1000 = ''
    count = 0
    for tmp in sqlList:
        sql_1000 += tmp
        count += 1
        if count >= 1000:
            #sql_1000_list.append(sql_1000)
            #print(sql_1000)
            mysql_write(sql_1000)
            time.sleep(4)
            count = 0
            sql_1000 = ''
    if sql_1000:
        #sql_1000_list.append(sql_1000)
        #print(sql_1000)
        mysql_write(sql_1000)

def mysql_write(sql):
    # mysql
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='',
        db='shares',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    cur = conn.cursor()
    # print(sql)
    count = 0
    try:
        cur.execute(sql)
    except Exception:
        count += 1
        print('Error: {}'.format(count))
    cur.close()
    conn.commit()
    conn.close()


if __name__ == '__main__':
    read_sql()