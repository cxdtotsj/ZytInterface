'''
问答类接口
继承api_data.py
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from util.assert_judgment import AssertJudgment
from base.public_param import PublicParam
from util.operation_json import OperetionJson
from data.get_data import SQLData
import time
import unittest
from data.api_data import QaApiData as QAData


class TestQA(unittest.TestCase, QAData):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_assert = AssertJudgment()
        cls.get_data = SQLData()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id
        cls.e_id = cls.pub_param.get_expert_info()[1]
        cls.e_token = cls.pub_param.get_expert_info()[0]
        cls.opera_json = OperetionJson("../dataconfig/zyt_data.json")

    def test01_01_qa_qSubmit_noEid(self):
        """case01-01 : 向专家提问 ;
           缺少专家 ID """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": "",
                "title": QAData.qa_title,
                "description": QAData.qa_desc,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40001",
            "返回的errno不正确")

    def test01_02_qa_qSubmit_noExpert(self):
        """case01-02 : 向专家提问 ;
           专家不存在 """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": "@#￥%……",
                "title": QAData.qa_title,
                "description": QAData.qa_desc,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40007",
            "返回的errno不正确")

    def test01_03_qa_qSubmit_noTitle(self):
        """case01-03 : 向专家提问 ;
           问题题目为空 """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id,
                "description": QAData.qa_desc,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40002",
            "返回的errno不正确")

    def test01_04_qa_qSubmit_noDesc(self):
        """case01-04 : 向专家提问 ;
           问题描述为空 """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id,
                "title": QAData.qa_title,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40003",
            "返回的errno不正确")

    def test01_05_qa_qSubmit_noAnswer(self):
        """case01-05 : 向专家提问 ;
           专家未开启回答 """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id,
                "title": QAData.qa_title,
                "description": QAData.qa_desc,
                "img": QAData.qa_img_one}
        sql = '''update zyt_user set is_open_ask = 0 where user_id = '{}';'''.format(
            self.e_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40004",
            "返回的errno不正确")

    def test01_06_qa_qSubmit_imgNum(self):
        """case01-06 : 向专家提问 ;
           问题图片超过3 张 """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id,
                "title": QAData.qa_title,
                "description": QAData.qa_desc,
                "img": QAData.qa_img_four}
        sql = '''update zyt_user set is_open_ask = 1 where user_id = '{}';'''.format(
            self.e_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40006",
            "返回的errno不正确")

    def test01_07_qa_qSubmit_expertStatus(self):
        """case01-07 : 向专家提问 ;
           专家未通过认证 """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id,
                "title": QAData.qa_title,
                "description": QAData.qa_desc,
                "img": QAData.qa_img_one}
        sql = '''update zyt_user set professor_status = 0 where user_id = '{}';'''.format(
            self.e_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40008",
            "返回的errno不正确")

    def test01_08_qa_qSubmit_success(self):
        """case01-08 : 向专家提问 ;
           问题提问成功 """
        api = "/api/v1/qa/qsubmit"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id,
                "title": QAData.qa_title,
                "description": QAData.qa_desc,
                "img": QAData.qa_img_one}
        sql = '''update zyt_user set professor_status = 1 where user_id = '{}';'''.format(
            self.e_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data, headers=QAData.qa_headers)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertIsNotNone(res_dict["data"]["last_id"], "未返回提问问题的id")
        # 返回问题的id至json文件
        self.opera_json.check_json_value(
            "test_01_08_qa_submit_success", res_dict["data"]["last_id"])

    def test02_01_qa_aSubmit_errorStatus(self):
        """case02-01 : 向专家提问 ;
           非待回答状态 """
        api = "/api/v1/qa/asubmit"
        qid = self.opera_json.get_data("test_01_08_qa_submit_success")

        data = {"user_id": self.e_id,
                "token": self.e_token,
                "qid": qid,
                "answer_content": QAData.answer_content,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40011",
            "返回的errno不正确")

    def test02_02_qa_aSubmit_noId(self):
        """case02-02 : 向专家提问 ;
           问题 id 为空 """
        api = "/api/v1/qa/asubmit"
        data = {"user_id": self.e_id,
                "token": self.e_token,
                "answer_content": QAData.answer_content,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40009",
            "返回的errno不正确")

    def test02_03_qa_aSubmit_errorId(self):
        """case02-03 : 向专家提问 ;
           问题 id 不存在 """
        api = "/api/v1/qa/asubmit"
        data = {"user_id": self.e_id,
                "token": self.e_token,
                "qid": "@#$%",
                "answer_content": QAData.answer_content,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40010",
            "返回的errno不正确")

    def test02_04_qa_aSubmit_noContent(self):
        """case02-04 : 向专家提问 ;
           回答内容为空 """
        api = "/api/v1/qa/asubmit"
        qid = self.opera_json.get_data("test_01_08_qa_submit_success")
        # 购买问题，7s后专家再作答
        self.get_data.zyt_pay_order(
            self.user_id, self.token, qid, 2, 0, "#/expert/payment")
        time.sleep(7)
        data = {"user_id": self.e_id,
                "token": self.e_token,
                "qid": qid,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40012",
            "返回的errno不正确")

    def test02_05_qa_aSubmit_imgNum(self):
        """case02-05 : 向专家提问 ;
           回答图片超过 3 张 """
        api = "/api/v1/qa/asubmit"
        qid = self.opera_json.get_data("test_01_08_qa_submit_success")
        data = {"user_id": self.e_id,
                "token": self.e_token,
                "qid": qid,
                "answer_content": QAData.answer_content,
                "img": QAData.qa_img_four}
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40013",
            "返回的errno不正确")

    def test02_06_qa_aSubmit_noAnswer(self):
        """case02-06 : 向专家提问 ;
           专家回答已关闭 """
        api = "/api/v1/qa/asubmit"
        qid = self.opera_json.get_data("test_01_08_qa_submit_success")

        data = {"user_id": self.e_id,
                "token": self.e_token,
                "qid": qid,
                "answer_content": QAData.answer_content,
                "img": QAData.qa_img_one}
        sql = '''update zyt_user set is_open_ask = 0 where user_id = '{}';'''.format(
            self.e_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40016",
            "返回的errno不正确")

    def test02_07_qa_aSubmit_success(self):
        """case02-07 : 向专家提问 ;
           专家回答成功 """
        api = "/api/v1/qa/asubmit"
        qid = self.opera_json.get_data("test_01_08_qa_submit_success")

        data = {"user_id": self.e_id,
                "token": self.e_token,
                "qid": qid,
                "answer_content": QAData.answer_content,
                "img": QAData.qa_img_one}
        sql = '''update zyt_user set is_open_ask = 1 where user_id = '{}';'''.format(
            self.e_id)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    # 再次作答的错误码应为 -40014
    def test02_08_qa_aSubmit_answerAgain(self):
        """case02-08 : 向专家提问 ;
           专家再次回答 """
        api = "/api/v1/qa/asubmit"
        qid = self.opera_json.get_data("test_01_08_qa_submit_success")

        data = {"user_id": self.e_id,
                "token": self.e_token,
                "qid": qid,
                "answer_content": QAData.answer_content,
                "img": QAData.qa_img_one}
        res = self.run_method.post(api, data, headers=QAData.qa_headers)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-40014",
            "返回的errno不正确")

    def test03_01_qa_detail_isBuy(self):
        """case03-01 : 某个问题的详情
           已购买该问题 """
        qid = self.opera_json.get_data("test_01_08_qa_submit_success")
        api = "/api/v1/qa/detail/{}".format(qid)
        data = {"user_id": self.user_id,
                "token": self.token, }
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertTrue(
            "answer_content" in res_dict["data"].keys(),
            "已购买问题未返回问题答案")

    def test04_01_qa_list_default(self):
        """case04-01 : 问题大厅-问题列表;
            不传数量和页面参数，默认页面为 1，数量为 10 """
        api = "/api/v1/qa/list"
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api,data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where ask_status in (1,5) ORDER by created_at DESC'''
        ask_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 10, ask_num)

    def test04_02_qa_list_specified(self):
        """case04-02 : 问题大厅-问题列表;
            指定参数 """
        api = "/api/v1/qa/list"
        data = {"user_id": self.user_id,
                "token": self.token,
                "l": 15,
                "p": 2}
        res = self.run_method.get(api,data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where ask_status in (1,5) ORDER by created_at DESC'''
        ask_num = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], data["p"], "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], ask_num)

    def test04_03_qa_list_search(self):
        """case04-03 : 问题大厅-问题列表;
            指定 搜索 参数 """
        api = "/api/v1/qa/list"
        data = {"user_id": self.user_id,
                "token": self.token,
                "k": "提问"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertTrue(len(res_dict["data"]["data"]) >= 1, "搜索的课程数不正确")

    def test05_01_qa_expert_default(self):
        """case05-01 : 专家的过往问答;
            不传数量，默认返回 7 """
        api = "/api/v1/qa/expert"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id}
        res = self.run_method.get(api,data)
        res_dict = res.json()
        sql = '''select id from zyt_user_answer where user_id = '{}';'''.format(self.e_id)
        answer_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]), 7, answer_num)

    def test05_02_qa_expert_specified(self):
        """case05-02 : 专家的过往问答;
            指定参数 """
        api = "/api/v1/qa/expert"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": self.e_id,
                "l": 10}
        res = self.run_method.get(api,data)
        res_dict = res.json()
        sql = '''select id from zyt_user_answer where user_id = '{}';'''.format(self.e_id)
        answer_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]), data["l"], answer_num)

    def test06_01_qa_recom_default(self):
        """case06-01 : 首页-全部优质问答;
            不传数量，默认返回 12 """
        api = "/api/v1/qa/recom"
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api,data)
        res_dict = res.json()
        sql = '''select id from zyt_user_answer where user_id = '{}';'''.format(self.e_id)
        answer_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]), 12, answer_num)

    def test06_02_qa_recom_specified(self):
        """case06-02 : 首页-全部优质问答;
            指定参数 """
        api = "/api/v1/qa/recom"
        data = {"user_id": self.user_id,
                "token": self.token,
                "l": 18}
        res = self.run_method.get(api,data)
        res_dict = res.json()
        sql = '''select id from zyt_user_answer where user_id = '{}';'''.format(self.e_id)
        answer_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]), data["l"], answer_num)
