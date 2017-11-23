#!/usr/bin/env python
# coding=utf-8
__author__ = 'NoControl'
__date__ = '2017/9/30'
# sys_demo.py sys解释器相关函数
# 该模块含有解释器的一些变量，与解释器交互的函数

import sys

# Python3 sys（解释器 模块）
def sys_demo():
    # 默认编码
    print(sys.getdefaultencoding())

    # Python版本
    print(sys.version)

    # 添加模块路径到搜索路径
    sys.path.append("./module")

    # (函数)打印异常信息
    try:
        1/0
    except:
        types, value, back = sys.exc_info()  # 捕获异常
        sys.excepthook(types, value, back)

    # 输入和输出
    sys.stdout.write(">> ")
    sys.stdout.flush()
    strs = sys.stdin.readline()[:-1]
    sys.stderr.write("输入的内容为：{}".format(strs))
    sys.stderr.flush()

def sys_func():
    lists = sys.argv  # 传递给Python脚本的命令行参数列表 => python p.py -> ['p.py'] / python
    strs = sys.getdefaultencoding()  # 默认字符集名称
    num = sys.getfilesystemencoding()  # 系统文件名字符集名称
    dicts = sys.getrefcount(object)  # 返回object的引用计数（比实际多1个）
    lists = sys.path  # 模块搜索路径
    sys.path.append("./test")  # 动态添加模块搜索路径
    strs = sys.platform  # 平台标识符（系统身份进行详细的检查，推荐使用） Linux: 'linux' / Windows:'win32' / Cygwin:'cygwin' / Mac OS X:'darwin'
    strs = sys.version  # python解释器版本
    lists = sys.thread_info  # 线程信息
    num = sys.api_version  # 解释器C API版本

    types, value, back = sys.exc_info()  # 捕获异常 详见 异常 文章
    sys.excepthook(types, value, back)  # 打印异常
    types = sys.last_type
    value = sys.last_value
    back = sys.last_trackback
    # sys.exit([arg])  // 引发SystemExit异常退出Python(可以try)，范围[0,127], None==0, "string"==1
    sys.exit(0)

    num = sys.getrecursionlimit()  # 最大递归数（堆栈最大深度）
    sys.setrecursionlimit(5000)  # 修改最大递归数

    fnum = sys.getswitchinterval()  # 获取线程切换间隔
    sys.setswitchinterval(0.005)  # 设置线程切换间隔，单位秒
    num = sys.getcheckinterval()  # 解释器的检查间隔
    sys.setcheckinterval(100)  # 设置解释器检查间隔，执行（默认）100个虚拟指令执行一次检查, 值为<=0时,检查每个虚拟指令

    # sys.stdin // 标准输入流
    strs = sys.stdin.readline()[:-1]
    # sys.stdout // 标准出入输出
    sys.stdout.write(">>")
    sys.stdout.flush()
    # sys.stderr // 标注错误流
    sys.stderr.write(">>")

    # ---

    lists = sys.builtin_module_names  # 所有模块 (注:非导入模块)
    path = sys.base_exec_prefix  # Python安装路径
    path = sys.base_prefix  # 同base_exec_prefix
    path = sys.exec_prefix  # 同base_exec_prefix
    path = sys.prefix  # 同base_exec_prefix
    path = sys.executable  # Python解释器的绝对路径

    strs = sys.byteorder  # 本机字节顺序指示器, big-endian(最高有效字节在第一位)值为'big', little-endian(最低有效字节在第一位)值为'little'
    strs = sys.copyright  # python版权
    num = sys.hexversion  # 16进制版本号
    lists = sys.implementation  # 当前运行的解释器的信息
    num = sys.getallocatedblocks()  # 解释器当前分配的内存块的数量
    boolean = sys.dont_write_bytecode  # 是否不会尝试导入源模块是写入.pyc文件 (False会写入.pyc文件)
    # sys.getsizeof(object[, default]) // 返回对象的大小bit, 只计算自身内存消耗,不计算引用对象的内存消耗, 调用对象的__sizeof__(), default没有获取到默认返回值
    num = sys.getsizeof(object)
    boolean = sys.is_finalizing()  # 解释器是否正在被关机
    num = sys.maxsize  # 最大整数值(2 ** 31 -1), 与系统有关
    num = sys.maxunicode  # 最大Unicode值的整数 (1114111)
    strs = sys.ps1  # 解释器主提示符
    strs = sys.ps2  # 解释器次提示符

    sys.call_tracing(func, ("arg",))  # 调用函数
    sys._clear_type_cache()  # 清除内部类型缓存
    sys._debugmallocstats()  # 打印CPython内存分配器状态的低级信息

    sys.setprofile(profilefunc)  # 设置profile函数, 默认None
    sys.getprofile()  # 获取profile函数
    sys.settrace(tracefunc)  # 设置跟踪函数, def tracefunc(frame、event 和arg):
    sys.gettrace()  # 获取跟踪函数, 默认None
    sys.set_coroutine_wrapper(wrapper)  # 设置包装 def wrapper(coro):
    sys.get_coroutine_wrapper()  # 包装, 默认None


if __name__ == "__main__":
    sys_demo()

    sys_func()


"""
*之后需要复习的模块复习
"""


# 听说这段代码很酷炫，学完试试
'''
# ! /usr/bin/python
# _*_ coding: utf-8 _*_
import sys

from colorama import init
init(strip=not sys.stdout.isatty())
from termcolor import cprint
from pyfiglet import figlet_format

cprint(figlet_format('welcome', fonta='starwars'),
        'yellow', 'on_blue', attrs=['bold'])
'''

