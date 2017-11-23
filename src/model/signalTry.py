"""
Python模块之（signal）
signal包负责在Python程序内部处理信号，典型的操作包括预设信号
处理函数，暂停并等待信号，以及定时发出SIGALRM等。要注意，signal包
主要是针对UNIX平台（比如Linux，MAC OS），而Windows内核中由于
对信号机制的支持不充分，所以在Windows上的Python不能发挥信号系统的功能
信号（signal）-- 进程之间通讯的方式，是一种软件中断。一个进程一旦接收到信号就会
打断原来的程序执行流程来处理信号
"""
# 定义信号名
# signal包定义了各个信号名及其对应的整数，比如：
import signal
print(signal.SIGABRT)
print(signal.SIG_DFL)
# Python所用的信号名与Linux一致，可以通过$ man 7 signal 查询

# 预设信号处理函数
# signal包的核心是使用signal.signal()函数来预设（register）信号处理函数，如下所示：
# signal.signal(signalnum, handler)  //好像写法不太对？？？
# signaknum为某个信号，handle为该信号的处理函数。 我们在信号基础里提到，进程可以无视信号
# 可以采取默认操作，还可以自定义操作。当handler为signal.SIG_IGN时，信号被无视（ignore）。
# 当handler为signal.SIG_DFL,进程采取默认操作（default）。当handler为一个函数名时，进程采取函数
# 中定义的操作。

# Define signal handler function

"""
def myHandler(signum, frame):
    print('I received: ', signum)
"""

# register signal.SIGTSTP's handler
"""
signal.signal(signal.SIGTSTP, myHandler())
signal.pause()
print('End of Signal Demo')
"""
# 有问题待测试

# signal.signal()  预设信号处理函数
# signal.pause()  让该进程暂停以等待信号
"""
在主程序中，我们首先使用signal.signal()函数来预设信号处理函数。然后我们执行signal.pause()来让该进程暂停以等待信号， 以等待信号。当信号SIGUSR1被传递给该进程时，进程从暂停中恢复，并根据预设，执行SIGTSTP的信号处理函数myHandler()。 myHandler的两个参数一个用来识别信号(signum)，另一个用来获得信号发生时，进程栈的状况(stack frame)。这两个参数都是由signal.singnal()函数来传递的。

上面的程序可以保存在一个文件中(比如test.py)。我们使用如下方法运行:

$python test.py

以便让进程运行。当程序运行到signal.pause()的时候，进程暂停并等待信号。此时，通过按下CTRL+Z向该进程发送SIGTSTP信号。我们可以看到，进程执行了myHandle()函数, 随后返回主程序，继续执行。(当然，也可以用$ps查询process ID, 再使用$kill来发出信号。)

(进程并不一定要使用signal.pause()暂停以等待信号，它也可以在进行工作中接受信号，比如将上面的signal.pause()改为一个需要长时间工作的循环。)

我们可以根据自己的需要更改myHandler()中的操作，以针对不同的信号实现个性化的处理。
"""

# 定时发出SIGALRM信号
# 一个有用的函数是signal.alarm(), 它被用于在一定时间之后，向进程自身发送SIGALRM信号

# Define signal handler function
def myHandler(signum, frame):
    print("Now, it's the time")
    exit()

# register signal.SIGALRM's handler
signal.signal(signal.SIGALRM, myHandler)
signal.alarm(5)
while True:
    print('not yet')

# python3 不支持
# 我们这里用了一个无限循环以便让进程持续运行。在signal.alarm()执行5秒之后，
# 进程将向自己发出SIGALRM信号，随后，信号处理函数myHandler开始执行。

# 总结
# signal.SIG*
# signal.signal()
# signal.alarm() 不支持
