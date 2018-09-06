'''
2018-9-5
问答类接口
用户user_id : d5eba536a06411e8b6e30017fa004b58
专家id ：f350756baf4211e8b6e30017fa004b58
已回答问题id : 260
未回答问题id : 227
test06~test10为 提问-支付-专家回答-提起申诉场景
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from base.public_param import PublicParam
from util.operation_json import OperetionJson
from base.getURL import API
import datetime
import time
import unittest


class TestQA(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id
        cls.get_url = API()
        cls.opera_json = OperetionJson("../dataconfig/zyt_data.json")

    @classmethod
    def tearDownClass(cls):
        cls.opera_db.close_db()

    def test01_QaRecom(self):
        '''首页-全部热门专家'''

        api = "/api/v1/qa/recom"
        data = {"user_id": self.user_id,
                "token": self.token,
                "l": 12}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        try:
            self.assertEqual(len(res_dict["data"]), 12)
        except BaseException:
            print("首页的优质回答数不足12个")

    def test02_QaExpert(self):
        '''某专家的过往问答'''

        api = "/api/v1/qa/expert"
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": "f350756baf4211e8b6e30017fa004b58",
                "l": 7}

        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select ask_id from zyt_user_answer where user_id = 'f350756baf4211e8b6e30017fa004b58';'''
        ask_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if ask_num >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]), data["l"], "返回的专家回答数量不正确")
        elif 1 <= ask_num < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]) < data["l"],
                "返回的专家回答数量不正确")
        else:
            self.assertTrue(len(res_dict["data"]) == 0, "专家没有回答")

    def test03_QaList(self):
        '''问题大厅-问题列表'''

        api = "/api/v1/qa/list"
        data = {"user_id": self.user_id,
                "token": self.token,
                "p": 1,
                "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where ask_status in (1,5) ORDER by created_at DESC'''
        ask_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if ask_num >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的问题数不正确")
        elif 1 <= ask_num < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的问题数不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "没有已回答的问题")

    def test04_QaDetailBuy(self):
        '''某个问题详情（已购买问题）'''

        api = "/api/v1/qa/detail/260"
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

    def test05_QaDetailNoBuy(self):
        '''某个问题详情（未购买问题）'''

        api = "/api/v1/qa/detail/227"
        data = {"user_id": self.user_id,
                "token": self.token, }
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertFalse(
            "answer_content" in res_dict["data"].keys(),
            "未购买的问题返回问题答案")

    def test06_QaQSubmit(self):
        '''向专家提问'''

        api = "/api/v1/qa/qsubmit"
        qa_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        qa_title = "这是问题题目 -- %s" % qa_time
        qa_desc = "这是问题描述 -- %s" % qa_time
        data = {"user_id": self.user_id,
                "token": self.token,
                "eid": "f350756baf4211e8b6e30017fa004b58",
                "title": qa_title,
                "description": qa_desc,
                "img": ["/1536116758846885506?imageView2/2/w/212/h/136/q/100"]}
        headers = {"content-type": "application/json"}
        res = self.run_method.post(api, data, headers=headers)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertIsNotNone(res_dict["data"]["last_id"], "未返回提问问题的id")

        # 返回问题id
        self.opera_json.check_json_value(
            "test06_QaQSubmit", res_dict["data"]["last_id"])

    def test07_Pay(self):
        '''购买商品（2-提问类）'''

        api = "/api/v1/pay/pay"
        good_id = self.opera_json.read_data()["test06_QaQSubmit"]
        return_url = self.get_url.http_api_url("#/expert/payment")
        data = {"user_id": self.user_id,
                "token": self.token,
                "paymethod": 1,
                "paychannel": "web",
                "good_id": good_id,
                "good_type": 2,
                "amount": 0,
                "returnurl": return_url}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["token"], self.token, "返回的token不一致")

    def test08_ExpertLogin(self):
        '''专家账号登陆，获取user_id,token'''

        api = "/api/v1/user/login"
        data = {"mobile": 18317026527, "password": "Password01!"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        # 保存专家的user_id，token信息至json
        expert_data = {"user_id": "", "token": ""}
        expert_data["user_id"] = res_dict["data"]["user_id"]
        expert_data["token"] = res_dict["data"]["token"]
        self.opera_json.check_json_value("test08_ExpertLogin", expert_data)
        time.sleep(7)

    def test09_QaASubmit(self):
        '''专家回答提问'''

        api = "/api/v1/qa/asubmit"
        qid = self.opera_json.get_data("test06_QaQSubmit")
        answer_content = "这是问题答案 -- %s" % (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = {"user_id": self.opera_json.get_data("test08_ExpertLogin")["user_id"],
                "token": self.opera_json.get_data("test08_ExpertLogin")["token"],
                "qid": qid,
                "answer_content": answer_content}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test10_MyQuesionAppeal(self):
        '''对专家问答进行申诉'''

        api = "/api/v1/user/myquesionappeal"
        qid = self.opera_json.read_data()["test06_QaQSubmit"]
        appeal_content = "这是问题申诉内容 -- %s" % (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = {"user_id": self.user_id,
                "token": self.token,
                "qid": qid,
                "appeal_content": appeal_content}
        res = self.run_method.post(api,data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())


if __name__ == '__main__':
    unittest.main()