'''
2018-9-4
专家类接口
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from base.public_param import PublicParam
import unittest


class TestExpert(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id

    @classmethod
    def tearDownClass(cls):
        cls.opera_db.close_db()

    def test01_ExpertRecom(self):
        '''首页-全部热门专家'''

        api = "/api/v1/expert/recom"
        data = {"l": 6}

        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(len(res_dict["data"]),
                         data["l"], "返回的热门专家不足%s个" % (data["l"]))

    def test02_ExpertSkill(self):
        '''专家列表页-专业筛选项'''

        api = "/api/v1/expert/skill"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_skill_config where status = 1;'''
        skill_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(len(res_dict["data"]), skill_num, "返回的专业刷选项数目不正确")

    def test03_List(self):
        '''专家列表页-专家可筛选列表(带翻页)'''

        api = "/api/v1/expert/list"
        data = {"l": 10,
                "p": 1}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user where professor_status != 0 and user_status = 1;'''
        expert_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if expert_num >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的专家数量不正确")
        elif 1 <= expert_num < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的专家数量不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "没有专家")
