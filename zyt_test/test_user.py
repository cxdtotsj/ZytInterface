'''
2018-9-3
用户类接口
用户账号 ： 18321829313
'''

from base.baseMethod import BaseMethod
from data.get_data import SQLData
from util.operation_db import OperationDB
from base.public_param import PublicParam
import datetime
import random
import unittest


class TestUser(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.get_data = SQLData()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id

    def test01_01_user_login_errorMobile(self):
        """case01-01 : 用户-登录;
            用户不存在  """
        api = "/api/v1/user/login"
        data = {"mobile": 111111111,
                "password":"Password02!"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(res_dict["code"],0,"登陆校验失败")

    def test01_02_user_login_errorPwd(self):
        """case01-02 : 用户-登录;
            用户密码错误  """
        api = "/api/v1/user/login"
        data = {"mobile": 18321829313,
                "password":"Password01!"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(res_dict["code"],0,"登陆校验失败")

    def test01_03_user_login_success(self):
        """case01-02 : 用户-登录;
            用户账号、密码正确  """
        api = "/api/v1/user/login"
        data = {"mobile": 18321829313,
                "password":"Password02!"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(res_dict["data"]["user_id"],self.user_id,"用户user_id返回不正确")

    def test02_01_user_likes_noAskId(self):
        """case02-01 : 点赞 ;
           问题ID 为空 """
        api = "/api/v1/user/likes"
        data = {"user_id": self.user_id,
                "token": self.token,
                "type": 1,
                "act": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40020",
            "返回的errno不正确")

    def test02_02_user_likes_errorAskId(self):
        """case02-02 : 点赞 ;
           问题ID 不存在 """
        api = "/api/v1/user/likes"
        data = {"user_id": self.user_id,
                "token": self.token,
                "relation_id": "@#$",
                "type": 1,
                "act": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40010",
            "返回的errno不正确")

    def test02_03_user_likes_noBuy(self):
        """case02-03 : 点赞 ;
           问题未购买 """
        api = "/api/v1/user/likes"
        # qid_noBuy = self.get_data.get_ask()
        data = {"user_id": self.user_id,
                "token": self.token,
                "relation_id": 327,
                "type": 1,
                "act": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40021",
            "返回的errno不正确")