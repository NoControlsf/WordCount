import configparser
import string, os, sys

cf = configparser.ConfigParser()

cf.read("sharesDB.conf")

#return all section
secs = cf.sections()
print('sections:', secs)

opts = cf.options("db")
print('options:', opts)

kvs = cf.items("db")
print('db:', kvs)

#read by type
db_host = cf.get("db", "db_host")
db_port = cf.getint("db", "db_port")
db_user = cf.get("db", "db_user")
db_pass = cf.get("db", "db_pass")

#read int
threads = cf.getint("concurrent", "thread")
processors = cf.getint("concurrent", "processor")

print("db_host:", db_host)
print("db_port:", db_port)
print("db_user:", db_user)
print("db_pass:", db_pass)

print("thread:", threads)
print("processor:", processors)


#modify one value and write to file 修改
# cf.set("db", "db_pass", "xgmtest")
# cf.write(open("sharesDB.conf", "w"))