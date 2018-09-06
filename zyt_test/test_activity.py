'''
2018-9-1
活动类接口
活动表：zyt_event ; id = 48
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from util.operation_json import OperetionJson
from base.public_param import PublicParam
import time
import unittest


class TestActivityView(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_json = OperetionJson()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id
        # 需要报名的活动id（后期可通过数据库新增一个活动，并返回至json）
        cls.event_id = 49
        # 不需要报名的活动id
        cls.no_event_id = 48
        cls.api = "/api/v1/activity/signup"

    @classmethod
    def tearDownClass(cls):
        cls.opera_db.close_db()

    def test01_Activity(self):
        '''获取活动详情 case1'''

        api = '/api/v1/activity/48'
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''SELECT event_title,event_content FROM zyt_event where id = 48;'''
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

    def test02_Banner(self):
        '''活动中心-已启用&置顶的活动列表'''

        api = "/api/v1/activitys/banner"
        data = {"l": 3}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select * from zyt_event where event_rank != 0 and event_status = 1;'''
        activity_banner = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if not activity_banner:
            raise RuntimeError("未设置已启用的置顶活动")
        self.assertIn(len(res_dict["data"]), (1, 2, 3), "返回的置顶活动数不正确")

    def test03_Recom(self):
        '''活动单页-已启用&非置顶的推荐活动列表'''

        api = "/api/v1/activitys/recom"
        data = {"l": 10}
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test04_List(self):
        '''活动中心-已启用&非置顶的全部活动列表(带翻页)'''

        api = "/api/v1/activitys/list"
        data = {"l": 5,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 2, "返回的页数不正确")
        try:
            self.assertEqual(len(res_dict["data"]["data"]), 5)
        except BaseException:
            print("第二页的活动数不足5个")

    def test05_New(self):
        '''活动中心-已启用的最新活动'''
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


class TestActivitySignUp(unittest.TestCase):
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
        cls.event_id = 49
        # 不需要报名的活动id
        cls.no_event_id = 48
        cls.api = "/api/v1/activity/signup"

    @classmethod
    def tearDownClass(cls):
        cls.db = OperationDB()
        cls.opera_json = OperetionJson()
        # 获取活动id（通过数据库）
        cls.event_id = 49
        # 删除已报名的活动记录(通过event_id删除)
        user_eventSql = '''delete from zyt_user_event where event_id = {};'''.format(cls.event_id)
        cls.db.delete_data(user_eventSql)
        # 更新活动数据（后期可直接删除该活动）
        after_time = int(time.time()+1000)
        after_sql = '''update zyt_event set end_time = {},event_status= 1 where id = {};'''.format(after_time,cls.event_id)
        cls.db.update_data(after_sql)
        cls.db.close_db()

    def test01_no_user(self):
        '''case01 : 缺少user_id参数'''

        data = {"token": self.token,
                "id": self.event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-10001",
            "返回的errno不正确")

    def test02_no_token(self):
        '''case02 : 缺少token参数'''

        data = {"user_id": self.user_id,
                "id": self.event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-10001",
            "返回的errno不正确")

    def test03_error_user(self):
        '''case03 : 错误的user_id参数'''

        data = {"user_id": "{}1".format(self.user_id),
                "token": self.token,
                "id": self.event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-10002",
            "返回的errno不正确")

    def test04_error_token(self):
        '''case04 : 错误的token参数'''

        data = {"user_id": self.user_id,
                "token": "{}1".format(self.token),
                "id": self.event_id}
        res = self.run_method.post(self.api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-10002",
            "返回的errno不正确")

    def test05_no_eventIdKey(self):
        '''case05 : 缺少活动id'''

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

    def test06_no_event_idValue(self):
        '''case06 : 活动id不存在'''

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

    def test07_sign_event_success(self):
        '''case07 : 活动报名成功'''

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

    def test08_repeat_sign_event(self):
        '''case08 : 重复报名'''

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

    def test09_event_timeout(self):
        '''case09 : 活动报名时间已截止'''

        before_time = int(time.time()-1000)
        sql = '''update zyt_event set end_time = {} where id = {};'''.format(before_time,self.event_id)
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


    def test10_event_offline(self):
        '''case10 : 活动已下线'''

        sql = '''update zyt_event set event_status = 0 where id = {};'''.format(self.event_id)
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

    def test11_not_sign_event(self):
        '''case11 : 不需要报名的活动'''

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

    def test12_fail_sign_event(self):
        '''
        case12 : 报名活动失败，
        暂时无法抛出错误code
        '''
        pass

    def test13_full_sign_event(self):
        '''
        case13 : 该活动已达到报名上限，
        超过设置的人数后，仍可以点击报名
        '''
        pass


if __name__ == "__main__":
    unittest.main()
