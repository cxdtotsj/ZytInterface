'''
2018-9-3
用户类接口
用户账号 ： 18321829313
专家账号： 18317026527
'''

from base.baseMethod import BaseMethod
from data.get_data import SQLData
from util.operation_db import OperationDB
from util.assert_judgment import AssertJudgment
from base.public_param import PublicParam
from util.operation_json import OperetionJson
from data.api_data import UserApiData as User
import time
import unittest


class TestUser(unittest.TestCase, User):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_assert = AssertJudgment()
        cls.get_data = SQLData()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id
        cls.eid = cls.pub_param.get_expert_info()[1]
        cls.etoken = cls.pub_param.get_expert_info()[0]
        cls.opera_json = OperetionJson("../dataconfig/zyt_data.json")

    def test04_01_user_login_errorMobile(self):
        """case04-01 : 用户-登录;
            用户不存在  """
        api = "/api/v1/user/login"
        data = {"mobile": 111111111,
                "password": "Password02!"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(res_dict["code"], 0, "登陆校验失败")

    def test04_02_user_login_errorPwd(self):
        """case04-02 : 用户-登录;
            用户密码错误  """
        api = "/api/v1/user/login"
        data = {"mobile": User.user_phone,
                "password": "Password01!"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(res_dict["code"], 0, "登陆校验失败")

    def test04_03_user_login_success(self):
        """case04-03 : 用户-登录;
            用户账号、密码正确  """
        api = "/api/v1/user/login"
        data = {"mobile": User.user_phone,
                "password": "Password02!"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            res_dict["data"]["user_id"],
            self.user_id,
            "用户user_id返回不正确")

    def test05_01_user_likes_noAskId(self):
        """case05-01 : 点赞 ;
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

    def test05_02_user_likes_errorAskId(self):
        """case05-02 : 点赞 ;
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

    def test05_03_user_likes_Buy(self):
        """case05-03 : 点赞 ;
           点赞已购买问题 """
        api = "/api/v1/user/likes"
        # 购买问题
        qid = self.get_data.get_ask(self.user_id, self.token, self.eid)
        data = {"user_id": self.user_id,
                "token": self.token,
                "relation_id": qid,
                "type": 1,
                "act": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        # 返回qid至json文件
        self.opera_json.check_json_value("test02_03_user_likes_Buy", qid)

    def test05_04_user_likes_again(self):
        """case05-04 : 点赞 ;
           再次点赞 """
        api = "/api/v1/user/likes"
        qid_buy = self.opera_json.get_data("test02_03_user_likes_Buy")
        data = {"user_id": self.user_id,
                "token": self.token,
                "relation_id": qid_buy,
                "type": 1,
                "act": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40024",
            "返回的errno不正确")

    def test05_05_user_likes_again(self):
        """case05-05 : 点赞 ;
           取消点赞 """
        api = "/api/v1/user/likes"
        qid_buy = self.opera_json.get_data("test02_03_user_likes_Buy")
        data = {"user_id": self.user_id,
                "token": self.token,
                "relation_id": qid_buy,
                "type": 1,
                "act": "cancel"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test05_06_user_likes_again(self):
        """case05-06 : 点赞 ;
           再次取消点赞 """
        api = "/api/v1/user/likes"
        qid_buy = self.opera_json.get_data("test02_03_user_likes_Buy")
        data = {"user_id": self.user_id,
                "token": self.token,
                "relation_id": qid_buy,
                "type": 1,
                "act": "cancel"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40023",
            "返回的errno不正确")

    def test06_01_user_feedback_noContent(self):
        """case06-01 : 用户反馈 ;
           未填写反馈内容 """
        api = "/api/v1/user/feedback"
        data = {"user_id": self.user_id,
                "token": self.token}

        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50030",
            "返回的errno不正确")

    def test06_02_user_feedback_success(self):
        """case06-02 : 用户反馈 ;
           用户反馈成功 """
        api = "/api/v1/user/feedback"
        data = {"user_id": self.user_id,
                "token": self.token,
                "feed_content": User.feed_content}
        res = self.run_method.post(api, data)

        sql = '''select content from zyt_user_feedback where user_id = '{}' ORDER BY created_at desc;'''.format(
            self.user_id)
        new_content = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(new_content["content"], User.feed_content, "反馈内容未提交")

    def test07_01_user_defaultEdit_noData(self):
        """case07-01 : 个人资料编辑，不是专家 ;
           参数为空 """
        api = "/api/v1/user/edit"
        data = {"user_id": self.user_id,
                "token": self.token}
        # 确认不是专家
        sql = '''update zyt_user set professor_status = 0,professor_certificate_verify = 0
                          where user_id = '{}';'''.format(self.user_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50012",
            "返回的errno不正确")

    def test07_02_user_defaultEdit_errorType(self):
        """case07-02 : 个人资料编辑，不是专家 ;
           编辑类型不存在 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default11",
            "savedata": {
                "nickname": User.nick_name}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50011",
            "返回的errno不正确")

    def test07_03_user_defaultEdit_noNickName(self):
        """case07-03 : 个人资料编辑，不是专家 ;
           昵称为空 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": None}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50013",
            "返回的errno不正确")

    def test07_04_user_defaultEdit_phone(self):
        """case07-04 : 个人资料编辑，不是专家 ;
           手机号无法修改 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "mobile": 11111111111}}
        res = self.run_method.post(api, data, headers=User.headers)
        sql = '''select phone from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        update_phone = self.opera_db.get_fetchone(sql)["phone"]

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertNotEqual(
            update_phone,
            data["savedata"]["mobile"],
            "手机号已被更新成功")

    def test07_06_user_defaultEdit_success(self):
        """case07-06 : 个人资料编辑，不是专家 ;
           修改个人资料 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "name": "bear chen"}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test07_07_user_defaultEdit_errorEmail(self):
        """case07-07 : 个人资料编辑，不是专家 ;
           修改个人资料 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "email": "acb#bac.com"}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50017",
            "返回的errno不正确")

    def test07_08_user_defaultEdit_emailSuccess(self):
        """case07-08 : 个人资料编辑，不是专家 ;
           修改个人资料 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "email": "xdchen@123.com"}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test08_01_user_verifyEdit_noName(self):
        """case08-01 : 申请专家认证，不是专家 ;
           姓名为空 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "verify",
            "savedata": {
                "nickname": User.nick_name,
                "name": None}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50014",
            "返回的errno不正确")

    def test08_02_user_verifyEdit_noSkill(self):
        """case08-02 : 申请专家认证，不是专家 ;
           专业为空 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "verify",
            "savedata": {
                "nickname": User.nick_name,
                "name": "bear chen",
                "skill_id": None,
                "cert": ["/abc"]}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50015",
            "返回的errno不正确")

    def test08_03_user_verifyEdit_noAvatar(self):
        """case08-03 : 申请专家认证，不是专家 ;
           证书为空 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "verify",
            "savedata": {
                "nickname": User.nick_name,
                "name": "bear chen",
                "skill_id": 1,
                "cert": []}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50018",
            "返回的errno不正确")

    def test08_04_user_verifyEdit_uploadVer(self):
        """case08-04 : 申请专家认证，不是专家 ;
           提交证书 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "verify",
            "savedata": {
                "nickname": User.nick_name,
                "name": "bear chen",
                "skill_id": 1,
                "cert": ["/abc"]}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test08_05_user_verifyEdit_uploadAgain(self):
        """case08-05 : 申请专家认证，不是专家 ;
           再次提交证书 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "verify",
            "savedata": {
                "nickname": User.nick_name,
                "name": "bear chen",
                "skill_id": 1,
                "cert": ["/abcd"]}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50019",
            "返回的errno不正确")

    def test08_06_user_verifyEdit_nameAgain(self):
        """case08-06 : 申请专家认证，认证中 ;
           修改专家姓名 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "name": "bear1chen"}}
        sql = '''select 'name' from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        update_name = self.opera_db.get_fetchone(sql)["name"]
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertNotEqual(update_name, data["savedata"]["name"], "姓名已被更新成功")

    def test08_07_user_verifyEdit_skillAgain(self):
        """case08-07 : 申请专家认证，认证中 ;
           修改专家技能 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "skill_id": 2}}
        sql = '''select skill from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        update_skill = self.opera_db.get_fetchone(sql)["skill"]
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertNotEqual(
            update_skill,
            data["savedata"]["skill_id"],
            "技能已被更新成功")

    def test08_08_user_verifyExpert_nameAgain(self):
        """case08-08 : 申请专家认证，已是专家 ;
           修改专家姓名 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "name": "bear1chen"}}
        sql_expert = '''update zyt_user set professor_status = 1,professor_certificate_verify = 2
                            where user_id = '{}';'''.format(self.user_id)
        self.opera_db.update_data(sql_expert)
        sql_name = '''select 'name' from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        update_name = self.opera_db.get_fetchone(sql_name)["name"]
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertNotEqual(update_name, data["savedata"]["name"], "姓名已被更新成功")

    def test08_09_user_verifyEdit_skillAgain(self):
        """case08-07 : 申请专家认证，已是专家 ;
           修改专家技能 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": User.nick_name,
                "skill_id": 2}}
        sql = '''select skill from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        update_skill = self.opera_db.get_fetchone(sql)["skill"]
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertNotEqual(
            update_skill,
            data["savedata"]["skill_id"],
            "技能已被更新成功")

    def test09_01_user_uploadEdit_avatar(self):
        """case09-01 : 申请专家认证，已是专家 ;
           修改头像为空 """
        api = "/api/v1/user/edit"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "upload",
            "savedata": {
                "nickname": User.nick_name,
                "avatar": None}}
        res = self.run_method.post(api, data, headers=User.headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50016",
            "返回的errno不正确")

    def test10_01_user_myOpenQA_noType(self):
        """case10-01 : 开启专家咨询，设置价格 ;
           咨询开关为空"""
        api = "/api/v1/user/myopenqa"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "type": None}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50029",
            "返回的errno不正确")

    def test10_02_user_myOpenQA_errorPrice(self):
        """case10-02 : 开启专家咨询，设置价格 ;
           设置非数字咨询价格"""
        api = "/api/v1/user/myopenqa"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "type": "open",
            "price": "abc"}
        res = self.run_method.post(api, data)
        sql = '''select ask_price from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        ask_price = self.opera_db.get_fetchone(sql)["ask_price"]

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(ask_price, 0, "价格更新失败")

    def test10_03_user_myOpenQA_noExpert(self):
        """case10-03 : 开启专家咨询，设置价格 ;
           非专家开启咨询"""
        api = "/api/v1/user/myopenqa"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "type": "open"}
        sql = '''update zyt_user set professor_status = 0 and is_open_ask = 0
                  where user_id = '{}';'''.format(self.user_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50031",
            "返回的errno不正确")

    def test10_04_user_myOpenQA_setPrice(self):
        """case10-04 : 开启专家咨询，设置价格 ;
           设置咨询价格"""
        api = "/api/v1/user/myopenqa"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "type": "open",
            "price": 0}
        sql = '''update zyt_user set professor_status = 1 where user_id = '{}';'''.format(
            self.user_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test10_05_user_myOpenQA_close(self):
        """case10-05 : 开启专家咨询，设置价格 ;
           关闭咨询"""
        api = "/api/v1/user/myopenqa"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "type": "close",
            "price": 5}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test10_06_user_myOpenQA_closeAgain(self):
        """case10-06 : 开启专家咨询，设置价格 ;
           再次关闭咨询"""
        api = "/api/v1/user/myopenqa"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "type": "close",
            "price": 0}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test11_01_user_follow_notExpert(self):
        """case11-01 : 关注某用户 ;
           被关注用户不是专家"""
        api = "/api/v1/user/follow"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "follow_user_id": self.eid,
            "t": "add"}
        # 清楚已关注数据
        sql_clear = '''delete from zyt_user_attention
                  where user_id = '{}' and attention_user_id = '{}';'''.format(self.user_id, self.eid)
        self.opera_db.delete_data(sql_clear)
        sql_expert = '''update zyt_user set professor_status = 0
                          where user_id = '{}';'''.format(self.eid)
        self.opera_db.update_data(sql_expert)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50021",
            "返回的errno不正确")

    def test11_02_user_follow_nofId(self):
        """case11-02 : 关注某用户 ;
           被关注用户id 为空"""
        api = "/api/v1/user/follow"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "follow_user_id": None,
            "t": "add"}
        sql_expert = '''update zyt_user set professor_status = 1
                          where user_id = '{}';'''.format(self.eid)
        self.opera_db.update_data(sql_expert)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50006",
            "返回的errno不正确")

    def test11_03_user_follow_errorFId(self):
        """case11-03 : 关注某用户 ;
           被关注用户id 不存在"""
        api = "/api/v1/user/follow"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "follow_user_id": self.eid + 'abc',
            "t": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50007",
            "返回的errno不正确")

    def test11_04_user_follow_success(self):
        """case11-04 : 关注某用户 ;
           关注用户成功 """
        api = "/api/v1/user/follow"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "follow_user_id": self.eid,
            "t": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test11_05_user_follow_again(self):
        """case11-05 : 关注某用户 ;
           已关注该用户 """
        api = "/api/v1/user/follow"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "follow_user_id": self.eid,
            "t": "add"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50008",
            "返回的errno不正确")

    def test11_06_user_follow_again(self):
        """case11-06 : 关注某用户 ;
           取消关注用户 """
        api = "/api/v1/user/follow"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "follow_user_id": self.eid,
            "t": "cancel"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test11_07_user_follow_again(self):
        """case11-07 : 关注某用户 ;
           再次取消关注用户 """
        api = "/api/v1/user/follow"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "follow_user_id": self.eid,
            "t": "cancel"}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50010",
            "返回的errno不正确")

    def test12_01_user_saveProject_noP_name(self):
        """case12-01 : 新增作品 ;
           项目名称为空 """
        api = "/api/v1/user/saveproject"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "p_name": None,
            "p_desc": User.p_desc,
            "p_img": User.p_img}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50001",
            "返回的errno不正确")

    def test12_02_user_saveProject_noP_desc(self):
        """case12-02 : 新增作品 ;
           项目简介为空 """
        api = "/api/v1/user/saveproject"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "p_name": User.p_name,
            "p_desc": None,
            "p_img": User.p_img}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50002",
            "返回的errno不正确")

    def test12_03_user_saveProject_noP_img(self):
        """case12-03 : 新增作品 ;
           项目图片为空 """
        api = "/api/v1/user/saveproject"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "p_name": User.p_name,
            "p_desc": User.p_desc,
            "p_img": None}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50003",
            "返回的errno不正确")

    def test12_04_user_saveProject_success(self):
        """case12-04 : 新增作品 ;
           项目上传成功 """
        api = "/api/v1/user/saveproject"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "p_name": User.p_name,
            "p_desc": User.p_desc,
            "p_img": User.p_img}
        '''清除项目'''
        sql = '''DELETE from zyt_user_project where user_id = '{}';'''.format(
            self.user_id)
        self.opera_db.delete_data(sql)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        return res

    def test12_05_user_saveProject_more20(self):
        """case12-05 : 新增作品 ;
           上传项目超过20个 """
        for i in range(20):
            res = self.get_data.get_project(self.user_id, self.token)
            self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
            if res.json()["result"] == "fail":
                self.assertEqual(
                    self.run_method.get_errno(res),
                    "-50005",
                    "返回的errno不正确")
            else:
                self.assertEqual(self.run_method.get_result(res),
                                 "success", res.json())

    def test13_01_user_dynamicList_default(self):
        """case13-01 : 用户动态列表(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 10 """
        api = "/api/v1/user/dynamiclist/{}".format(self.user_id)
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_dynamics where user_id = '{}' ORDER BY created_at DESC;'''.format(
            self.user_id)
        dynamic_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 10, dynamic_num)

    def test13_02_user_dynamicList_specified(self):
        """case13-02 : 用户动态列表(带翻页);
            指定参数 """
        api = "/api/v1/user/dynamiclist/{}".format(self.user_id)
        data = {"user_id": self.user_id,
                "token": self.token,
                "l": 15,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_dynamics where user_id = '{}' ORDER BY created_at DESC;'''.format(
            self.user_id)
        dynamic_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["current_page"],
            data["p"],
            "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], dynamic_num)

    def test14_01_user_myMessage_default(self):
        """case14-01 : 我的站内消息(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 10 """
        api = "/api/v1/user/mymessage"
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_message where user_id = '{}';'''.format(
            self.user_id)
        message_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["list"]["data"]), 10, message_num)

    def test14_02_user_myMessage_specified(self):
        """case14-02 : 用户动态列表(带翻页);
            指定参数 """
        api = "/api/v1/user/mymessage"
        data = {"user_id": self.user_id,
                "token": self.token,
                "l": 15,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_message where user_id = '{}';'''.format(
            self.user_id)
        message_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["list"]["data"]), data["l"], message_num)

    def test15_01_user_myFollow_default(self):
        """case15-01 : 我的关注(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/myfollow"
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_attention where user_id = '{}';'''.format(
            self.user_id)
        follow_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, follow_num)

    def test15_02_user_myFollow_specified(self):
        """case15-02 : 我的关注(带翻页);
            指定参数 """
        api = "/api/v1/user/myfollow"
        data = {"user_id": self.user_id,
                "token": self.token,
                "l": 15,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_attention where user_id = '{}';'''.format(
            self.user_id)
        follow_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["current_page"],
            data["p"],
            "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], follow_num)

    def test15_03_user_myFollow_search(self):
        """case15-03 : 我的关注(带翻页);
            指定 搜索 参数 """
        api = "/api/v1/user/myfollow"
        data = {"user_id": self.user_id,
                "token": self.token,
                "k": "t"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)

    def test16_01_user_projectList_default(self):
        """case16-01 : 用户项目作品列表(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 6 """
        api = "/api/v1/user/projectlist/{}".format(self.user_id)
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_project where user_id = '{}';'''.format(
            self.user_id)
        project_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 6, project_num)

    def test16_02_user_projectList_specified(self):
        """case16-02 : 用户项目作品列表(带翻页);
            指定参数 """
        api = "/api/v1/user/projectlist/{}".format(self.user_id)
        data = {"user_id": self.user_id,
                "token": self.token,
                "l": 15,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_project where user_id = '{}';'''.format(
            self.user_id)
        dynamic_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["current_page"],
            data["p"],
            "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], dynamic_num)

    def test17_01_user_detail_noUser(self):
        """case01 : 用户详情
            缺少user_id参数"""
        api = "/api/v1/user/detail/{}".format(self.user_id)
        data = {"token": self.token}
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-10001",
            "返回的errno不正确")

    def test17_02_user_detail_noToken(self):
        """case01 : 用户详情
            缺少token 参数"""
        api = "/api/v1/user/detail/{}".format(self.user_id)
        data = {"user_id": self.user_id}
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-10001",
            "返回的errno不正确")

    def test17_03_user_detail_success(self):
        """case01 : 用户详情
           登陆成功 """
        api = "/api/v1/user/detail/{}".format(self.user_id)
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test18_01_user_myAnswerWait_default(self):
        """case18-01 : 我的待回答(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/myanswer"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "wait"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where ask_status = 0 and answer_user_id = '{}';'''.format(
            self.user_id)
        wait_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, wait_num)

    def test18_02_user_myAnswerWait_specified(self):
        """case18-02 : 我的待回答(带翻页);
            指定参数 """
        api = "/api/v1/user/myanswer"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "wait",
                "l": 15,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where ask_status = 0 and answer_user_id = '{}';'''.format(
            self.user_id)
        wait_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["current_page"],
            data["p"],
            "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], wait_num)

    def test18_03_user_myAnswerWait_search(self):
        """case18-03 : 我的待回答(带翻页);
            指定 搜索 参数 """
        api = "/api/v1/user/myanswer"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "wait",
                "l": 15,
                "p": 2,
                "k": "答案"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)

    def test19_01_user_myAnswerDone_default(self):
        """case19-01 : 我的已回答(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/myanswer"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "done"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_answer where user_id = '{}';'''.format(
            self.user_id)
        done_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, done_num)

    def test19_02_user_myAnswerDone_specified(self):
        """case19-02 : 我的已回答(带翻页);
            指定参数 """
        api = "/api/v1/user/myanswer"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "done",
                "l": 15,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_answer where user_id = '{}';'''.format(
            self.user_id)
        done_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["current_page"],
            data["p"],
            "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], done_num)

    def test19_03_user_myAnswerDone_search(self):
        """case19-03 : 我的已回答(带翻页);
            指定 搜索 参数 """
        api = "/api/v1/user/myanswer"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "done",
                "k": "答案"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)

    def test20_01_user_myQuestionAsk_default(self):
        """case20-01 : 我问的问题(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/myquestion"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "ask"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask
                  where user_id = '{}' and ask_status in (0,1,2,5);'''.format(self.user_id)
        ask_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, ask_num)

    def test20_02_user_myQuestionAsk_specified(self):
        """case20-02 : 我问的问题(带翻页);
            指定参数 """
        api = "/api/v1/user/myquestion"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "ask",
                "l": 15,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask
                  where user_id = '{}' and ask_status in (0,1,2,5);'''.format(self.user_id)
        ask_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], ask_num)

    def test20_03_user_myQuestionAsk_search(self):
        """case20-03 : 我问的问题(带翻页);
            指定 搜索 参数 """
        api = "/api/v1/user/myquestion"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "ask",
                "k": "答案"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)

    def test21_01_user_myQuestionBuy_default(self):
        """case21-01 : 我购买的问题(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/myquestion"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "buy"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select ask_id from zyt_user_buy_ask where user_id = '{}';'''.format(
            self.user_id)
        buy_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, buy_num)

    def test22_01_user_myQuestionClose_default(self):
        """case22-01 : 我关闭的问题(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/myquestion"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": "close"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where user_id = '{}' and ask_status in (3,4);'''.format(
            self.user_id)
        close_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, close_num)

    def test23_01_user_myCourseBuy_default(self):
        """case23-01 : 我购买的课程(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/mycourse"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": 1}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select classes_id from zyt_user_classes where user_id = '{}' and status = 1;'''.format(
            self.user_id)
        buy_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, buy_num)

    def test24_01_user_myCourseCollect_default(self):
        """case24-01 : 我收藏的课程(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 12 """
        api = "/api/v1/user/mycourse"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select classes_id from zyt_user_classes
                  where user_id = '{}' and status = 2;'''.format(self.user_id)
        collect_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, collect_num)

    def test25_01_myQuestionAppeal_noQId(self):
        """case25-01 : 对专家问答进行申诉;
            未传问题id """
        api = "/api/v1/user/myquesionappeal"
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": None,
                "appeal_content": User.appeal_content}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50022",
            "返回的errno不正确")

    def test25_02_myQuestionAppeal_errorQId(self):
        """case25-02 : 对专家问答进行申诉;
            问题id 不存在"""
        api = "/api/v1/user/myquesionappeal"
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": "1bc",
                "appeal_content": User.appeal_content}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50023",
            "返回的errno不正确")

    def test25_03_myQuestionAppeal_errorStatus(self):
        """case25-03 : 对专家问答进行申诉;
            问题当前状态不可申诉 """
        api = "/api/v1/user/myquesionappeal"
        qid = self.get_data.get_ask(self.user_id, self.token, self.eid)
        time.sleep(7)
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": qid,
                "appeal_content": User.appeal_content}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50025",
            "返回的errno不正确")
        # 返回qid至json文件
        self.opera_json.check_json_value("test25_03_myQuestionAppeal_errorStatus", qid)

    def test25_04_myQuestionAppeal_noContent(self):
        """case25-04 : 对专家问答进行申诉;
            申诉内容为空 """
        api = "/api/v1/user/myquesionappeal"
        qid = self.opera_json.get_data("test25_03_myQuestionAppeal_errorStatus")
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": qid,
                "appeal_content": None}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50026",
            "返回的errno不正确")

    def test25_05_myQuestionAppeal_success(self):
        """case25-05 : 对专家问答进行申诉;
            申诉成功 """
        api = "/api/v1/user/myquesionappeal"
        qid = self.opera_json.get_data("test25_03_myQuestionAppeal_errorStatus")
        self.get_data.get_answer(self.eid, self.etoken, qid)
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": qid,
                "appeal_content": User.appeal_content}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test25_06_myQuestionAppeal_isAppealing(self):
        """case25-06 : 对专家问答进行申诉;
            该问题正在申诉 """
        api = "/api/v1/user/myquesionappeal"
        qid = self.opera_json.get_data("test25_03_myQuestionAppeal_errorStatus")
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": qid,
                "appeal_content": User.appeal_content}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-50024",
            "返回的errno不正确")

    def test25_07_myQuestionAppeal_isending(self):
        """case25-06 : 对专家问答进行申诉;
            申诉问题正在退款中 """
        api = "/api/v1/user/myquesionappeal"
        qid = self.opera_json.get_data("test25_03_myQuestionAppeal_errorStatus")
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": qid,
                "appeal_content": User.appeal_content}
        sql = '''update zyt_user_ask set ask_status = 6 where id ={};'''.format(
            qid)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40025",
            "返回的errno不正确")
