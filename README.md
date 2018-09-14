python版本3.6


依赖模块(pip)：
pip install request==2.19.1
pip install pymysql==0.9.2


基础配置：
1.setting.py 中配置 数据库、域名


运行顺序：
1.获取数据库配置，operation_db.py 能获取正确的数据库
2.运行 python before.py
3.运行测试脚本


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

discover(测试发现，默认需要进入脚本目录下):
-v ： 输出详细测试信息，比如 python -m unittest discover -v

-s : 执行发现测试脚本的目录，默认未当前目录(.)，
        比如 python -m unittest discover -v -s /home/bear/ZytInterface/zyt_test

-p : 模式匹配测试文件，比如 python -m unittest discover -p "test*.py"

-t directory : 工程的根目录下搜索可以执行的测试脚本，默认是当前目录，
                比如 python -m unittest discover -v -t /home/bear/ZytInterface/zyt_test



