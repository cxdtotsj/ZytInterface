from base.getURL import API
from base.baseMethod import BaseMethod
from util.operation_json import OperetionJson
import unittest
import json

class Test_Message(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.get_url = API()
        cls.run_method = BaseMethod()
        cls.opear_json = OperetionJson()

    def test01_CodeGen(self):
        print("run 获取验证码...")

        data_dict = {"identity":"18521358916"}
        proto_method = "./message.proto 10.241.11.4:6443 pb.Message/CodeGen"
        # 返回结果
        res = self.run_method.grpc(proto_method,data_dict)
        # 断言的验证
        try:
            self.assertIsInstance(res, dict, "未返回正确结果")
            self.assertIn("data", res, "未返回验证码字段")
            verify_code = res["data"]
            self.assertNotEqual(verify_code,'',"验证码为空")
            self.assertEqual(len(verify_code),6,"验证码长度不一致")
        except AssertionError as e:
            print(e)
        # 依赖字段返回至json中
        self.opear_json.check_json_value("test01_CodeGen_data", verify_code)

    def test02_CodeVerify(self):
        print("run 验证验证码...")

        verify_code = self.opear_json.read_data()["test01_CodeGen_data"]
        data_dict = {"identity": "18521358916","data":verify_code}
        proto_method = "./message.proto 10.241.11.4:6443 pb.Message/CodeVerify"
        # 返回结果
        res = self.run_method.grpc(proto_method,data_dict)
        # 断言的验证
        try:
            self.assertIsInstance(res, dict, "未返回正确结果")
            self.assertEqual(res,{},"返回错误")
        except AssertionError as e:
            print(e)

if __name__ == "__main__":
    unittest.main()