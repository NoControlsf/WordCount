# coding:utf-8

import logging
# 1.简单的将日志打印到屏幕
# logging.debug('This is debug message')
# logging.info('This is info message')
# logging.warning('This is warning message')
"""
默认情况下，logging将日志打印到屏幕，日志级别为WARNING；
日志级别大小关系为：CRITICAL > ERROR > WARNING > INFO > DEBUG > NOTSET ,
当然也可以自己定义日志级别
"""
# 2.通过logging.basicConfig函数对日志的输出格式及方式做相关配置
"""
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datafmt='%a, %d %b %Y %H:%M:%S',
                    filename='myapp.log',
                    filemode='w')
logging.debug('This is debug message')
logging.info('This is info message')
logging.warning('This is warning message')

错误日志：ValueError: Unrecognised argument(s): datafmt
应该是不支持python3
"""
"""
logging.basicConfig(filename='log1.log',
                    format='%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S %p',
                    level=logging.DEBUG)
while True:
    option = input("input a digit:")
    if option.isdigit():
        print("hehe", option)
        logging.info('option correct')
    else:
        logging.error("Must input a digit!")
"""
# logging.debug('有bug')
# logging.info('有新的信息')
# logging.warning('警告信息')
# logging.error('错误信息')
# logging.critical('紧急错误信息')
# logging.log(10, 'log')

logger = logging.getLogger("simple_example")
logger.setLevel(logging.DEBUG)

# 输出到屏幕
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)
# 输出到文件
fh = logging.FileHandler("log2.log")
fh.setLevel(logging.INFO)
# 设置日志格式
fomatter = logging.Formatter('%(asctime)s -%(name)s-%(levelname)s-%(module)s:%(message)s')
ch.setFormatter(fomatter)
fh.setFormatter(fomatter)
logger.addHandler(ch)
logger.addHandler(fh)

logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")