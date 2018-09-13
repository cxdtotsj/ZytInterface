'''
专家类接口
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from base.public_param import PublicParam
from util.assert_judgment import AssertJudgment
import unittest


class TestExpert(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_assert = AssertJudgment()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id

    def test01_01_expert_recom_default(self):
        """case01-01 : 首页-全部热门专家;
            不传数量，默认返回 6 """
        api = "/api/v1/expert/recom"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select user_id from zyt_user where professor_status != 0'''
        expert_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]), 6, expert_num)

    def test02_01_expert_skill(self):
        """case02-01 : 专家列表页-专业筛选项
           无参数 """

        api = "/api/v1/expert/skill"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_skill_config where status = 1;'''
        skill_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(len(res_dict["data"]),skill_num,"返回的专业数目不正确")

    def test03_01_expert_list_default(self):
        """case03-01 : 专家列表页-专家可筛选列表(带翻页);
            不传数量和页面参数，默认页面为 1，数量为 10 """
        api = "/api/v1/expert/list"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_user where professor_status != 0 and is_open_ask = 1 and user_status = 1;'''
        expert_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 10, expert_num)

    def test03_02_expert_list_specified(self):
        """case03-02 : 专家列表页-专家可筛选列表(带翻页);
            指定参数 """
        api = "/api/v1/expert/list"
        data = {"l": 15,
                "p": 2}
        res = self.run_method.get(api,data)
        res_dict = res.json()
        sql = '''select id from zyt_user where professor_status != 0 and is_open_ask = 1 and user_status = 1;'''
        expert_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], data["p"], "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], expert_num)

    def test03_03_expert_list_search(self):
        """case03-03 : 专家列表页-专家可筛选列表(带翻页);
            指定 搜索 参数 """
        api = "/api/v1/expert/list"
        data = {"k": "b"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertTrue(len(res_dict["data"]["data"]) >= 1, "搜索的课程数不正确")

    def test03_04_expert_list_skill(self):
        """case03-04 : 专家列表页-专家可筛选列表(带翻页);
            指定 专家专业 参数 """
        api = "/api/v1/expert/list"
        data = {"f": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user where professor_status!= 0 and is_open_ask = 1 and user_status = 1 and skill = 2;'''
        expert_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 10, expert_num)