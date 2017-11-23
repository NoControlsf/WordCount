# python中threading模块详解（一）
"""
threading提供了一个比thread模块更高层的API来提供线程的并发性。这些线程并发运行并共享内存
1、Thread的使用使用，目标函数可以实例化一个Thread对象，每个Thread对象代表着一个线程，可以通过start()
方法运行。
        这里对使用多线程和不适用多线程并发做了比较：
"""
# 首先是不使用多线程的操作：
"""
#!/usr/bin/python
#compare for multi threads
import time


def worker():
    print("worker")
    time.sleep(1)
    return

if __name__ == "__main__":
    for i in range(5):
        worker()
"""

# 下面是使用多线程并发的操作：

#!/usr/bin/python
import threading
import time


def worker():
    print("worker")
    time.sleep(1)
    return

for i in range(5):
    t = threading.Thread(target=worker)
    t.start()

# 可以明显看出使用了多线程并发的操作，花费时间要短很多。

# 2、threading.activeCount
