import os

#  python中os模块中常用的函数

print(os.name)  # 判断现在正在实用的平台，Windows 返回 ‘nt'; Linux 返回’posix'
print(os.getcwd())  # 得到当前工作的目录
print(os.listdir("."))  # 指定所有目录下所有的文件和目录名,以列表的形式全部列举出来，其中没有区分目录和文件。
# os.remove("C:/Users/NoControl/Downloads/E书说明.txt")  # 删除指定文件
# os.rmdir("C:/Users/NoControl/Downloads/123")  # 删除指定目录
# os.mkdir("C:/Users/NoControl/Downloads/123")  # 创建目录
# 注意：这样只能建立一层，要想递归建立可用：os.makedirs()
print(os.path.isfile("C:/Users/NoControl/Downloads/123"))  # 判断指定对象是否为文件。是返回True，否则False
print(os.path.isdir("C:/Users/NoControl/Downloads/123"))  # 判断指定对象是否为目录。是True，否则False
print(os.path.exists("C:/Users/NoControl/Downloads/123"))  # 检验指定的对象是否存在。是True,否则False
print(os.path.split("C:/Users/NoControl/Downloads/hamcrest-all-1.3.jar"))  # 返回路径的目录和文件名
# os.system("echo 'hello world!'") ----执行shell命令
# os.chdir() ----改变目录到指定目录
print(os.path.getsize("C:/Users/NoControl/Downloads/hamcrest-all-1.3.jar"))  # 或等文件的大小，如果为目录，返回0
print(os.path.abspath("."))  # 获得绝对路径
print(os.path.join('C:/Users/NoControl/Downloads', '11.jar'))  # 连接目录和文件名
print(os.path.basename("C:/Users/NoControl/Downloads/hamcrest-all-1.3.jar"))  # 返回文件名
print(os.path.dirname("C:/Users/NoControl/Downloads/hamcrest-all-1.3.jar"))  # 返回文件路径


