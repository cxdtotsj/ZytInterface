import datetime
import time
import sys
import os

# a = "这是一条评论 %s" %(datetime.datetime.now())
# print(a)
# print(type(a))

b = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
print(b)

# 获取当前时间戳
a = int(time.time()+1000)
print(a)

# 时间戳转换成时间
c = time.localtime(a)
d = time.strftime("%Y-%m-%d %H:%M:%S",c)
print(d)

# timeStamp = 1535791757
# timearrary = time.localtime(timeStamp)
# cuurrenttime = time.strftime("%Y-%m-%d %H:%M:%S",timearrary)
# print(cuurrenttime)
# print(type(cuurrenttime))

# curPath = os.path.abspath(os.path.dirname(__file__))
# rootPath = os.path.split(curPath)[0]
# time_now = datetime.datetime.now().date()
# filepath = r"{}\report\report{}.html".format(rootPath, time_now)
# file_name = filepath.split("report2")[1]
# true_name = "report2{}".format(file_name)
# print(true_name)
#
# class get_time:
#
#     def gettime(self):
#         time_test = datetime.datetime.now()
#         return time_test

