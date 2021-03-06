'''
活动类接口
class : TestActivityAView、TestActivityBSignUp
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from util.operation_json import OperetionJson
from base.public_param import PublicParam
from util.assert_judgment import AssertJudgment
from data.get_data import SQLData
import time
import unittest


class TestActivityAView(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_json = OperetionJson()
        cls.opera_assert = AssertJudgment()
        cls.get_data = SQLData()
        # 需要报名的活动id（后期可通过数据库新增一个活动，并返回至json）
        cls.event_id = cls.get_data.insert_event_yes()
        cls.opera_json.check_json_value("event_id",cls.event_id)
        time.sleep(3)
        # 不需要报名的活动id
        cls.no_event_id = cls.get_data.insert_event_no()
        cls.opera_json.check_json_value("no_event_id",cls.no_event_id)
        cls.api = "/api/v1/activity/signup"

    def test01_01_activity_detail(self):
        """case01-01 : 活动详情接口 """

        api = '/api/v1/activity/{}'.format(self.event_id)
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''SELECT event_title,event_content FROM zyt_event where id = {};'''.format(
            self.event_id)
        event_data = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["event_title"],
            event_data["event_title"],
            "接口返回的活动标题不正确")
        self.assertEqual(
            res_dict["data"]["event_content"],
            event_data["event_content"],
            "接口返回的活动内容不正确")


    def test02_01_activitys_banner_default(self):
        """case02-01 : 活动中心-已启用&置顶的活动列表接口；
            不传参，接口默认展示数量为3"""

        api = "/api/v1/activitys/banner"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_event where event_rank != 0 and event_status = 1;'''
        activity_banner = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']), 3, activity_banner)

    def test02_02_activitys_banner_specified(self):
        """case02-02 : 活动中心-已启用&置顶的活动列表接口；
            传入指定的参数"""

        api = "/api/v1/activitys/banner"
        data = {"l": 6}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_event where event_rank != 0 and event_status = 1;'''
        activity_banner = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']), data["l"], activity_banner)

    def test03_01_activitys_recom_default(self):
        """case03-01 : 活动单页-已启用&非置顶的推荐活动列表;
            不传参，接口默认展示数量为10 """

        api = "/api/v1/activitys/recom"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_event where event_rank = 0 and event_status = 1 ORDER BY created_time DESC;'''
        activity_recom = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']), 10, activity_recom)

    def test03_02_activitys_recom_specified(self):
        """case03-02 : 活动单页-已启用&非置顶的推荐活动列表;
            传入指定的参数 """

        api = "/api/v1/activitys/recom"
        data = {"l": 20}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_event where event_rank = 0 and event_status = 1 ORDER BY created_time DESC;'''
        activity_recom = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']), data["l"], activity_recom)

    def test04_01_activitys_list_default(self):
        """case04-01 : 活动中心-已启用&非置顶的全部活动列表(带翻页)；
            不传参，接口默认传 第一页，数量为20 """

        api = "/api/v1/activitys/list"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_event where event_rank = 0 and event_status = 1 ORDER BY created_time DESC;'''
        activity_list = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页面数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']["data"]), 20, activity_list)

    def test04_02_activitys_list_specified(self):
        """case04-02 : 活动中心-已启用&非置顶的全部活动列表(带翻页)；
            传入指定的参数 """

        api = "/api/v1/activitys/list"
        data = {"l": 20,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_event where event_rank = 0 and event_status = 1 ORDER BY created_time DESC;'''
        activity_list = self.opera_db.get_effect_row(sql)-data["l"]*(data["p"]-1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], data["p"], "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']["data"]), data["l"], activity_list)

    def test05_01_activitys_new_default(self):
        """case05-01 : 活动中心-已启用的最新活动"""

        api = "/api/v1/activitys/new"
        data = {"l": 1}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_event where  event_status = 1 ORDER BY created_time DESC;'''
        new_activity = self.opera_db.get_fetchone(sql)["id"]

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if not new_activity:
            raise RuntimeError("不存在活动")
        self.assertEqual(res_dict["data"][0]["id"], new_activity, "最新活动返回不正确")


class TestActivityBSignUp(unittest.TestCase):
    '''活动报名接口的case'''

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_json = OperetionJson()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id
        # 需要报名的活动id（可通过json去取活动id）
        cls.event_id = cls.opera_json.get_data("event_id")
        # 不需要报名的活动id
        cls.no_event_id = cls.opera_json.get_data("no_event_id")
        cls.api = "/api/v1/activity/signup"

    @classmethod
    def tearDownClass(cls):
        cls.db = OperationDB()
        cls.opera_json = OperetionJson()
        # 获取活动id（通过数据库）
        cls.event_id = cls.opera_json.get_data("event_id")
        cls.no_event_id = cls.opera_json.get_data("no_event_id")
        # 删除已报名的活动记录(通过event_id删除)
        user_eventSql = '''delete from zyt_user_event where event_id in ({},{});'''.format(
            cls.event_id,cls.no_event_id)
        cls.db.delete_data(user_eventSql)
        # 更新活动状态为已删除
        delete_event_sql = '''update zyt_event set event_status = -1 where id in ({},{});'''.format(
            cls.event_id, cls.no_event_id)
        cls.db.update_data(delete_event_sql)
        cls.db.close_db()

    def test06_01_activity_signUp_noId(self):
        """case06-01 : 缺少活动id """

        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-30001",
            "返回的errno不正确")

    def test06_02_activity_signUp_errorId(self):
        """case06-02 : 活动id不存在"""

        data = {"user_id": self.user_id,
                "token": self.token,
                "id": self.event_id + 100}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-30002",
            "返回的errno不正确")

    def test06_03_activity_signUp_success(self):
        """case06-03 : 活动报名成功"""

        data = {"user_id": self.user_id,
                "token": self.token,
                "id": self.event_id}
        res = self.run_method.post(self.api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_event where event_id = {} and user_id = '{}';'''.format(
            self.event_id, self.user_id)
        new_id = self.opera_db.get_fetchone(sql)["id"]

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["last_id"], new_id, "返回的已报名活动id不正确")

    def test06_04_activity_signUp_again(self):
        """case06-04 : 重复报名"""

        data = {"user_id": self.user_id,
                "token": self.token,
                "id": self.event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-30006",
            "返回的errno不正确")

    def test06_05_activity_signUp_outTime(self):
        """case06-05 : 活动报名时间已截止"""

        before_time = int(time.time() - 1000)
        sql = '''update zyt_event set end_time = {} where id = {};'''.format(
            before_time, self.event_id)
        self.opera_db.update_data(sql)

        data = {"user_id": self.user_id,
                "token": self.token,
                "id": self.event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-30008",
            "返回的errno不正确")

    def test06_06_activity_signUp_offline(self):
        """case06-06 : 活动已下线"""

        sql = '''update zyt_event set event_status = 0 where id = {};'''.format(
            self.event_id)
        self.opera_db.update_data(sql)

        data = {"user_id": self.user_id,
                "token": self.token,
                "id": self.event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-30003",
            "返回的errno不正确")

    def test06_07_activity_signUp_noSign(self):
        """case06-07 : 不需要报名的活动"""

        data = {"user_id": self.user_id,
                "token": self.token,
                "id": self.no_event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-30004",
            "返回的errno不正确")


if __name__ == "__main__":
    unittest.main()
