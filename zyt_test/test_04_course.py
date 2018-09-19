'''
课程类接口
class : TestCourse、TestSearchCourse

接口功能点 : 1.查看：首页热门课程、专业课选项、课程列表
             2.insert：线上课程、线上课时
                       线下课程、购买线下课程、查看下线课程二维码、收藏取消课程、发表评论、课程页面推荐位、查看课程的评论
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from util.operation_json import OperetionJson
from data.get_data import SQLData
from base.public_param import PublicParam
from util.assert_judgment import AssertJudgment
import unittest
import datetime
import time


class TestSearchCourse(unittest.TestCase):
    """课程查询类用例，不需要登陆"""

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.get_data = SQLData()
        cls.opera_assert = AssertJudgment()

    def test01_01_course_recom_default(self):
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

    def test01_02_course_recom_specified(self):
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

    def test03_01_course_list_default(self):
        """case03-01 : 培训页-课程可筛选列表(带翻页);
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
            self.get_data.array_get_dictValue(
                res_dict["data"]["data"], "id"), self.get_data.array_get_dictValue(
                new_course, "id"), "返回的id不一致")

    def test03_02_course_list_specified(self):
        """case03-02 : 培训页-课程可筛选列表(带翻页);
            传入指定的页数和单页数量 """

        api = "/api/v1/course/list"
        data = {"l": 5,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''SELECT id FROM zyt_classes where classes_status = 1 ORDER BY created_time DESC;'''
        new_course = self.opera_db.get_effect_row(
            sql) - data["l"] * (data["p"] - 1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["current_page"], data["p"], "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), data["l"], new_course)

    def test03_03_course_list_search(self):
        """case03-03 : 培训页-课程可筛选列表(带翻页);
            传入 搜索 参数（关键字设置为新增的课程名称） """

        api = "/api/v1/course/list"
        data = {"k": "这是"}
        res = self.run_method.get(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertTrue(len(res_dict["data"]["data"]) >= 1, "搜索的课程数不正确")

    def test03_04_course_list_online(self):
        """case03-04 : 培训页-课程可筛选列表(带翻页);
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

    def test03_05_course_list_offline(self):
        """case03-05 : 培训页-课程可筛选列表(带翻页);
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

    def test03_06_course_list_prof(self):
        """case03-06 : 培训页-课程可筛选列表(带翻页);
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

    def test03_07_course_list_salesSort(self):
        """case03-07 : 培训页-课程可筛选列表(带翻页);
            课程排序按 销量，排序规则默认为 desc  """
        api = "/api/v1/course/list"
        data = {"o": "sales"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes where classes_status = 1 ORDER BY buy_num DESC;'''
        sales_course = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, sales_course)

    def test03_08_course_list_salesSort(self):
        """case03-08 : 培训页-课程可筛选列表(带翻页);
            课程排序按 销量，排序规则为 asc  """
        api = "/api/v1/course/list"
        data = {"o": "sales",
                "s": "asc"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes where classes_status = 1 ORDER BY buy_num ASC;'''
        sales_course = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, sales_course)

    def test03_09_course_list_priceSort(self):
        """case03-09 : 培训页-课程可筛选列表(带翻页);
            课程排序按 价格，排序规则默认为 desc  """
        api = "/api/v1/course/list"
        data = {"o": "price"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes where classes_status = 1 ORDER BY classes_price DESC;'''
        price_course = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, price_course)

    def test03_10_course_list_priceSort(self):
        """case03-10 : 培训页-课程可筛选列表(带翻页);
            课程排序按 价格，排序规则默认为 desc  """
        api = "/api/v1/course/list"
        data = {"o": "price",
                "s": "asc"}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes where classes_status = 1 ORDER BY classes_price ASC;'''
        price_course = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.opera_assert.is_equal_value_len(
            len(res_dict["data"]["data"]), 12, price_course)


class TestCourse(unittest.TestCase):
    """线上、线下课程类用例"""

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_json = OperetionJson()
        cls.get_data = SQLData()
        cls.opera_assert = AssertJudgment()
        cls.pub_param = PublicParam()
        cls.token = cls.pub_param.token
        cls.user_id = cls.pub_param.user_id
        # 线上课程id，classes_type 为1
        cls.online_class = cls.get_data.insert_course(1)
        # 线上课时id，关联线上课程id
        cls.online_hour = cls.get_data.insert_course_hour(cls.online_class)
        # 线下课程id，classes_type 为2
        time.sleep(2)
        cls.offline_class = cls.get_data.insert_course(2)

    def test01_01_course_detail_default(self):
        """case01-01 : 查询课程详细内容;
            成功查询 """
        api = "/api/v1/course/detail/{}".format(self.online_class)
        data = {"token": self.token,
                "user_id": self.user_id}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes_hour where classes_id = {};'''.format(
            self.online_class)
        classes_hours = self.opera_db.get_fetchall(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        # 校验返回的课时id和数据库的是否一致
        self.assertEqual(
            self.get_data.array_get_dictValue(
                res_dict["data"]["hour"], "id"), self.get_data.array_get_dictValue(
                classes_hours, "id"), "返回的id不一致")

    def test01_02_course_detail_off(self):
        """case01-02 : 查询课程详细内容;
            课程已下架 """
        api = "/api/v1/course/detail/{}".format(self.online_class)
        data = {"token": self.token,
                "user_id": self.user_id}
        sql = '''update zyt_classes set classes_status = 0 where id = {};'''.format(
            self.online_class)
        self.opera_db.update_data(sql)
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20003",
            "返回的errno不正确")

    def test02_01_course_hourDetail_classesOff(self):
        """case02-01 : 查询线上课时的详细内容;
            课程已下架 """
        api = "/api/v1/course/hourdetail/{}".format(self.online_hour)
        data = {"token": self.token,
                "user_id": self.user_id}
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20003",
            "返回的errno不正确")

    def test02_02_course_hourDetail_classesBuy(self):
        """case02-02 : 查询线上课时的详细内容;
            需要购买课程，才能播放 """
        api = "/api/v1/course/hourdetail/{}".format(self.online_hour)
        data = {"token": self.token,
                "user_id": self.user_id}
        sql = '''update zyt_classes set classes_status = 1 where id = {};'''.format(
            self.online_class)
        self.opera_db.update_data(sql)
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20011",
            "返回的errno不正确")

    def test02_03_course_hourDetail_noContent(self):
        """case02-03 : 查询线上课时的详细内容;
            该课时视频不存在 """
        api = "/api/v1/course/hourdetail/{}".format(self.online_hour)
        data = {"token": self.token,
                "user_id": self.user_id}
        sql = '''update zyt_classes_hour set is_free = 1 where id = {};'''.format(
            self.online_hour)
        self.opera_db.update_data(sql)
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20015",
            "返回的errno不正确")

    def test_02_04_course_hourDetail_success(self):
        """case02-04 : 正常播放视频
        （未上传视频，无法播放，后期可以写个固定的视频url）"""
        pass

    def test03_01_course_qrCode_noID(self):
        """case03-01 : 线下课程二维码;
            课程 order_id 为空 """
        api = "/api/v1/course/qrcode"
        data = {}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20013",
            "返回的errno不正确")

    def test03_02_course_qrCode_errorID(self):
        """case03-02 : 线下课程二维码;
            课程order_id 不存在 """
        api = "/api/v1/course/qrcode"
        data = {"order_id": "@#$111"}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertIsNone(res_dict["data"], "返回的线下课程数据错误")

    def test03_03_course_qrCode_status(self):
        """case03-03 : 线下课程二维码;
            课程订单状态为 -1（失败） """
        api = "/api/v1/course/qrcode"
        returnurl = "#/train/{}".format(self.offline_class)
        # 购买课程
        order_id = self.get_data.zyt_pay_order(
            self.user_id, self.token, self.offline_class, 1, 0, returnurl)
        sql = '''update zyt_order set status = -1 where order_id = '{}';'''.format(
            order_id)
        self.opera_db.update_data(sql)
        data = {"order_id": order_id}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20014",
            "返回的errno不正确")

        # 返回order_id至json
        self.opera_json.check_json_value(
            "test03_03_course_qrCode_status", order_id)

    def test03_04_course_qrCode_status(self):
        """case03-04 : 线下课程二维码;
            课程订单状态为 1（待付款） """
        api = "/api/v1/course/qrcode"
        order_id = self.opera_json.get_data(
            "test03_03_course_qrCode_status")
        sql = '''update zyt_order set status = 1 where order_id = '{}';'''.format(
            order_id)
        self.opera_db.update_data(sql)
        data = {"order_id": order_id}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20014",
            "返回的errno不正确")

    def test03_05_course_qrCode_status(self):
        """case03-05 : 线下课程二维码;
            课程订单状态为 3（已关闭） """
        api = "/api/v1/course/qrcode"
        order_id = self.opera_json.get_data(
            "test03_03_course_qrCode_status")
        sql = '''update zyt_order set status = 3 where order_id = '{}';'''.format(
            order_id)
        self.opera_db.update_data(sql)
        data = {"order_id": order_id}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20014",
            "返回的errno不正确")

    def test03_06_course_qrCode_status(self):
        """case03-06 : 线下课程二维码;
            课程订单状态为 4（已退款） """
        api = "/api/v1/course/qrcode"
        order_id = self.opera_json.get_data(
            "test03_03_course_qrCode_status")
        sql = '''update zyt_order set status = 3 where order_id = '{}';'''.format(
            order_id)
        self.opera_db.update_data(sql)
        data = {"order_id": order_id}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20014",
            "返回的errno不正确")

    def test03_07_course_qrCode_status(self):
        """case03-07 : 线下课程二维码;
            课程订单状态为 2（已付款），查看线下课程二维码 """
        api = "/api/v1/course/qrcode"
        order_id = self.opera_json.get_data(
            "test03_03_course_qrCode_status")
        sql = '''update zyt_order set status = 2 where order_id = '{}';'''.format(
            order_id)
        self.opera_db.update_data(sql)
        data = {"order_id": order_id}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(res_dict["data"]["order_id"], order_id, "返回的订单号不正确")

    def test04_01_course_saveFavor_add_noID(self):
        """case04-01 : 收藏课程;
            课程 id 为空 """
        api = "/api/v1/course/savefavor"
        data = {
            "t": "add",
            "user_id": self.user_id,
            "token": self.token}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20001",
            "返回的errno不正确")

    def test04_02_course_saveFavor_add_errorID(self):
        """case04-02 : 收藏课程;
            不存在该课程 """
        api = "/api/v1/course/savefavor"
        data = {
            "id": self.offline_class+1000,
            "t": "add",
            "user_id": self.user_id,
            "token": self.token}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20002",
            "返回的errno不正确")

    def test04_03_course_saveFavor_add_off(self):
        """case04-03 : 收藏课程;
            该课程已下架 """
        api = "/api/v1/course/savefavor"
        data = {
            "id": self.offline_class,
            "t": "add",
            "user_id": self.user_id,
            "token": self.token}
        sql = '''update zyt_classes set classes_status = 0 where id = {};'''.format(self.offline_class)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20003",
            "返回的errno不正确")

    def test04_04_course_saveFavor_add_success(self):
        """case04-04 : 收藏课程;
            该课程收藏成功 """
        api = "/api/v1/course/savefavor"
        data = {
            "id": self.offline_class,
            "t": "add",
            "user_id": self.user_id,
            "token": self.token}
        sql = '''update zyt_classes set classes_status = 1 where id = {};'''.format(self.offline_class)
        self.opera_db.update_data(sql)
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(res_dict["data"]["token"],self.token,"返回的token不正确")

    def test04_05_course_saveFavor_add_again(self):
        """case04-05 : 收藏课程;
            该课程再次收藏 """
        api = "/api/v1/course/savefavor"
        data = {
            "id": self.offline_class,
            "t": "add",
            "user_id": self.user_id,
            "token": self.token}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20004",
            "返回的errno不正确")

    def test04_06_course_saveFavor_cancel_success(self):
        """case04-06 : 收藏课程;
            该课程取消收藏成功 """
        api = "/api/v1/course/savefavor"
        data = {
            "id": self.offline_class,
            "t": "cancel",
            "user_id": self.user_id,
            "token": self.token}
        res = self.run_method.post(api, data)
        res_dict = res.json()

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(res_dict["data"]["token"],self.token,"返回的token不正确")

    def test04_07_course_saveFavor_cancel_again(self):
        """case04-07 : 收藏课程;
            该课程再次取消收藏 """
        api = "/api/v1/course/savefavor"
        data = {
            "id": self.offline_class,
            "t": "cancel",
            "user_id": self.user_id,
            "token": self.token}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20012",
            "返回的errno不正确")

    def test05_01_course_commentSubmit_noID(self):
        """case05-01 : 发表课程评论;
            课程 id 为空 """
        api = "/api/v1/course/commentsubmit"
        content = "这是一条评论 %s" % (datetime.datetime.now())
        data = {
            "msg": content,
            "token": self.token,
            "user_id": self.user_id}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20001",
            "返回的errno不正确")

    def test05_02_course_commentSubmit_noContent(self):
        """case05-02 : 发表课程评论;
            评论内容 为空 """
        api = "/api/v1/course/commentsubmit"
        data = {
            "id": self.offline_class,
            "token": self.token,
            "user_id": self.user_id}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20006",
            "返回的errno不正确")

    def test05_03_course_commentSubmit_noBuy(self):
        """case05-03 : 发表课程评论;
            未购买该课程 """
        api = "/api/v1/course/commentsubmit"
        content = "这是一条评论 %s" % (datetime.datetime.now())
        data = {
            "id": self.online_class,
            "msg": content,
            "token": self.token,
            "user_id": self.user_id}
        res = self.run_method.post(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "fail", res.json())
        self.assertEqual(
            self.run_method.get_errno(res),
            "-20007",
            "返回的errno不正确")

    def test05_04_course_commentSubmit_success(self):
        """case05-04 : 发表课程评论;
            课程评论成功 """
        api = "/api/v1/course/commentsubmit"
        content = "这是一条评论 %s" % (datetime.datetime.now())
        data = {
            "id": self.offline_class,
            "msg": content,
            "token": self.token,
            "user_id": self.user_id}
        res = self.run_method.post(api, data)
        sql = '''select content from zyt_classes_comment where classes_id = {} ORDER BY created_at DESC;'''.format(self.offline_class)
        comment_content = self.opera_db.get_fetchone(sql)["content"]

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(comment_content, content, "课程评论未新增成功")

    def test06_01_course_commentList_default(self):
        """case06-01 : 课程的所有评论列表(带翻页)；
            不传参，接口默认传 第一页，数量为10 """
        api = "/api/v1/course/commentlist/{}".format(self.offline_class)
        res = self.run_method.get(api)
        res_dict = res.json()
        sql = '''select id from zyt_classes_comment where classes_id = {} ORDER BY created_at DESC;'''.format(self.offline_class)
        comment_list = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(res_dict["data"]["current_page"], 1, "返回的页面数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']["data"]), 10, comment_list)

    def test06_02_course_commentList_specified(self):
        """case06-02 : 课程的所有评论列表(带翻页)；
            传入指定传参 """
        api = "/api/v1/course/commentlist/{}".format(self.offline_class)
        data = {"l": 10,
                "p": 2}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_classes_comment where classes_id = {} ORDER BY created_at DESC;'''.format(self.offline_class)
        comment_list = self.opera_db.get_effect_row(sql)-data["l"]*(data["p"]-1)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(res_dict["data"]["current_page"], data["p"], "返回的页数不正确")
        self.opera_assert.is_equal_value_len(
            len(res_dict['data']["data"]), data["l"], comment_list)

    def test07_01_course_klyk_default(self):
        """case07-01 : 课程单页-看了又看推荐位;
            不传参，接口默认展示数量为6 """
        api = "/api/v1/course/klyk/{}".format(self.offline_class)
        res = self.run_method.get(api)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())

    def test07_02_course_klyk_specified(self):
        """case07-02 : 课程单页-看了又看推荐位;
            传入指定的参数 """
        api = "/api/v1/course/klyk/{}".format(self.offline_class)
        data = {"l": 10}
        res = self.run_method.get(api, data)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())


if __name__ == "__main__":
    unittest.main()
