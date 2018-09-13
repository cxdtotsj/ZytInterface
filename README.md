python版本3.6


依赖模块：
request==2.19.1
pymysql==0.9.2


基础配置：
1.setting.py 中配置 数据库、域名


运行顺序：
1.获取数据库配置，operation_db.py 能获取正确的数据库
2.运行 python before.py
3.


命令行运行测试用例(进入到用例目录)：
1.指定测试用例目录
unittest:
-b  --buffer : 在测试运行期间缓冲标准输出和标准错误流。通过测试期间的输出被丢弃。输出在测试失败或错误时正常回显，并添加到失败消息中。
-f --failfast : 在第一次错误或失败时停止测试运​​行。
-h --help : 给出所有的指令

(1) 运行目录下指定的py文件 test.py
python -m unittest  -v test.py

(2) 运行 test.py 下的 TestClass 类下的所有用例
python -m unittest -v test.TestClass

(3) 运行 test.py 下的 TestClass 类下的用例 test01
python -m unittest -v test.TestClass.test01


discover:
-v  --verbose : 详细输出
(1) 运行目录下所有的 test*.py 文件
python -m unittest discover -v



