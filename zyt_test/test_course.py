'''
2018-8-30
课程类接口
课程id = 32，为线上课程，已购买
课程id = 33，为线下课程，已购买
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from data.sql_data import SQLData
from base.public_param import PublicParam
from util.assert_judgment import AssertJudgment
import unittest
import datetime


class TestCourse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.sql_data = SQLData()
        cls.opera_assert = AssertJudgment()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id

    @classmethod
    def tearDownClass(cls):
        cls.opera_db.close_db()

    def test01_01_default_course_recom(self):
        """case01-01 : 首页-热门推荐课程列表;
            不传参，接口默认展示数量为8 """

        api = '/api/v1/course/recom'
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''SELECT id FROM `zyt_classes` where classes_status = 1;'''
        course_recom = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']), 8, course_recom)

    def test01_02_specified_course_recom(self):
        """case01-02 : 首页-热门推荐课程列表;
            传入指定的参数 """

        api = '/api/v1/course/recom'
        data = {"l": 15}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''SELECT id FROM `zyt_classes` where classes_status = 1;'''
        course_recom = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']), data["l"], course_recom)

    def test02_01_course_prof(self):
        """case02-01 : 培训页-课程专业筛选项"""

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

    def test03_01_default_course_list(self):
        """case03-01 : 培训页-课程可筛选列表(带翻页)
            不传参，默认页面为 1，数量为 12 """

        api = "/api/v1/course/list"
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''SELECT id FROM zyt_classes where classes_status = 1 ORDER BY created_time DESC;'''
        new_course = self.opera_db.get_fetchmany(sql, 12)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页数不正确")
        # 校验返回的课程id和数据库的是否一致（默认按最新排序）
        self.assertEqual(
            self.sql_data.array_get_dictValue(
                res_dict["data"]["data"], "id"), self.sql_data.array_get_dictValue(
                new_course, "id"), "返回的id不一致")

    def test03_02_specified_course_list(self):
        """case03-02 : 培训页-课程可筛选列表(带翻页)
            传入指定的页数和单页数量 """

        api = "/api/v1/course/list"
        data = {"l": 5,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''SELECT id FROM zyt_classes where classes_status = 1 ORDER BY created_time DESC;'''
        new_course = self.opera_db.get_effect_row(sql)-data["l"]*(data["p"]-1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["current_page"], data["p"], "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], new_course)

    def test03_03_search_course_list(self):
        """case03-03 : 培训页-课程可筛选列表(带翻页)
            传入 搜索 参数（关键字设置为新增的课程名称） """

        api = "/api/v1/course/list"
        data = {"k": "这是"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertTrue(len(res_dict["data"]["data"]) >= 1,"搜索的课程数不正确")

    def test03_04_course_online_list(self):
        """case03-04 : 培训页-课程可筛选列表(带翻页)
            传入 线上课程 类型参数 """

        api = "/api/v1/course/list"
        data = {"c": 1}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes where classes_status = 1 and classes_type = 1 ORDER BY created_time DESC;'''
        online_course = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, online_course)

    def test03_05_course_offline_list(self):
        """case03-05 : 培训页-课程可筛选列表(带翻页)
            传入 线下课程 类型参数 """

        api = "/api/v1/course/list"
        data = {"c": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes where classes_status = 1 and classes_type = 2 ORDER BY created_time DESC;'''
        offline_course = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, offline_course)

    def test03_06_course_prof_list(self):
        """case03-06 : 培训页-课程可筛选列表(带翻页)
            传入 多个课程专业 类型参数 """

        api = "/api/v1/course/list"
        data = {"f": "1|2"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes where classes_status = 1 and classes_cate_id in (1,2);'''
        prof_course = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, prof_course)



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
