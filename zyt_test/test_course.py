'''
2018-8-30
课程类接口
课程id = 32，为线上课程，已购买
课程id = 33，为线下课程，已购买
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from base.public_param import PublicParam
import unittest
import datetime


class TestCourse(unittest.TestCase):

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

    def test01_Recom(self):
        '''首页-热门推荐课程列表'''

        api = '/api/v1/course/recom'
        res = self.run_method.get(api)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(len(res_dict["data"]), 8, "返回的热门课程不足8个")

    def test02_Prof(self):
        '''培训页-课程专业筛选项'''

        api = "/api/v1/course/prof"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_classes_cate where classes_cate_status = 1;'''
        prof_row = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(len(res_dict["data"]), prof_row, "课程专业筛选项返回数量不正确")

    def test03_List(self):
        '''培训页-课程可筛选列表(带翻页)'''

        api = "/api/v1/course/list"
        data = {"l": 5, "p": 2}
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
            print("第二页的课程数量不足5个")

    def test04_CommentList32(self):
        '''课程id为32的课程评论(带翻页)'''

        sql = '''select id from zyt_classes where id = 32;'''
        classes_id = self.opera_db.get_fetchone(sql)
        if not classes_id:
            raise RuntimeError("未查询到该课程ID")
        api = "/api/v1/course/commentlist/32"
        data = {"l": 3, "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 2, "返回的页数不正确")
        try:
            self.assertEqual(len(res_dict["data"]["data"]), 3)
        except BaseException:
            print("第二页的课程评论数不足3个")

    def test05_Klyk32(self):
        '''课程id为32的页面内的推荐课程'''

        api = "/api/v1/course/klyk/32"
        data = {"l": 5}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select classes_id  from zyt_user_classes where status = 1 and user_id in (select DISTINCT user_id from zyt_user_classes where  classes_id = 32)'''
        klyk_classes_id = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if klyk_classes_id:
            try:
                self.assertEqual(len(res_dict["data"]), 5)
            except BaseException:
                print("购买该课程的用户，购买过的课程不足5个")

    def test06_CourseDetail(self):
        '''课程id为32的课程详细内容'''

        api = "/api/v1/course/detail/1"
        data = {"token": self.token, "user_id": self.user_id}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes_hour where classes_id = 32;'''
        class_hour_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            len(res_dict["data"]["hour"]), class_hour_num, "课时返回数量不正确")

    def test07_HourDetail(self):
        '''课时id为163的课时详细内容'''

        api = "/api/v1/course/hourdetail/163"
        data = {"token": self.token, "user_id": self.user_id}
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")

    def test08_QrCode(self):
        '''线下课程二维码'''

        api = "/api/v1/course/qrcode"
        data = {"order_id": "20180831161704248366"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["phone"],
            "18321829313",
            "该订单对应购买人不正确")

    def test09_SaveFavor(self):
        '''收藏取消课程'''

        api = "/api/v1/course/savefavor"
        sql = '''select classes_id from zyt_user_classes where classes_id = 32 and status = 2;'''
        classes_save = self.opera_db.get_fetchone(sql)
        if classes_save:
            data = {
                "id": 32,
                "t": "cancel",
                "user_id": self.user_id,
                "token": self.token}
        else:
            data = {
                "id": 32,
                "t": "add",
                "user_id": self.user_id,
                "token": self.token}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertTrue(res_dict["data"]["token"], "收藏或取消收藏失败")

    def test10_CommentSubmit(self):
        '''发表课程评论'''

        api = "/api/v1/course/commentsubmit"
        content = "这是一条评论 %s" % (datetime.datetime.now())
        data = {
            "id": 33,
            "msg": content,
            "token": self.token,
            "user_id": self.user_id}
        res = self.run_method.post(api, data)
        sql = '''select content from zyt_classes_comment where classes_id = 33 ORDER BY created_at DESC;'''
        update_content = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(update_content["content"], content, "课程评论未新增成功")


if __name__ == "__main__":
    unittest.main()
