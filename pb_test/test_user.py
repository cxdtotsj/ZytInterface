from base.getURL import API
from base.baseMethod import BaseMethod
from util.operation_json import OperetionJson
import unittest
import time


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_url = API()
        cls.run_method = BaseMethod()
        cls.opera_json = OperetionJson()

    # 只传mobile字段，获取一次性验证码
    def test01_Register(self):
        print("run 获取一次性验证码")

        data_dict = {"mobile":"18321829313"}
        proto_method = "./user.proto 10.241.11.4:6443 pb.User/Register"
        # 返回验证码
        res = self.run_method.grpc(proto_method,data_dict)
        #断言的验证
        try:
            self.assertIsInstance(res,dict,"未返回正确的结果")
            self.assertIn("code",res,"未返回验证码字段")
            verify_code = res["code"]
            self.assertNotEqual(verify_code,'',"验证码为空")
            self.assertEqual(len(verify_code),6,"验证码长度不正确")
        except AssertionError as e:
            print(e)
        # 把验证码写入json
        self.opera_json.check_json_value("test01_Register_code",verify_code)

    # 传入mobile + code + passwd,更改登陆密码，返回用户 id 及 token
    def test02_Register(self):
        print("run 手机+验证码+密码登陆,更改密码")

        verify_code = self.opera_json.read_data()["test01_Register_code"]
        data_dict = {"mobile":"18321829313",
                     "code":verify_code,
                     "passwd":"Password02!"}
        proto_method = "./user.proto 10.241.11.4:6443 pb.User/Register"
        # 获取返回结果
        res = self.run_method.grpc(proto_method,data_dict)
        #断言的验证
        try:
            self.assertIsInstance(res,dict,"未返回正确的结果")
            self.assertEqual(res["mobile"],data_dict["mobile"],"手机号不一致")
            self.assertEqual(res["passwd"],data_dict["passwd"],"密码未修改")
            self.assertTrue(res["session"],"session不存在")
            self.assertTrue(res["token"],"token不存在")
        except AssertionError as e:
            print(e)
        #获取所需返回值,写入json
        json_data = {"token":res["token"],
                     "passwd":res["passwd"],
                     "user_id":res["id"]
                     }
        self.opera_json.check_json_value("test02_Register",json_data)
        time.sleep(3)

    # 传入mobile + passwd,登陆，并获取token
    def test03_Register(self):
        print("run 使用新的密码登陆")

        new_passwd = self.opera_json.read_data()["test02_Register"]["passwd"]
        data_dict = {"mobile": "18321829313",
                     "passwd": new_passwd}
        proto_method = "./user.proto 10.241.11.4:6443 pb.User/Register"
        # 获取返回结果
        res = self.run_method.grpc(proto_method,data_dict)
        #断言的验证
        user_id = self.opera_json.read_data()["test02_Register"]["user_id"]
        test02_token = self.opera_json.read_data()["test02_Register"]["token"]
        try:
            self.assertIsInstance(res, dict, "未返回正确的结果")
            self.assertEqual(res["mobile"], data_dict["mobile"], "手机号不一致")
            self.assertEqual(res["id"],user_id,"用户不一致")
            self.assertNotEqual(res["token"],test02_token,"重新登陆后token未变更")
        except AssertionError as e:
            print(e)


if __name__ == "__main__":
    unittest.main()