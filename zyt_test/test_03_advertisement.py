'''
广告类接口
'''

import time
from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from util.assert_judgment import AssertJudgment
import unittest


class TestAdvertisement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.opera_assert = AssertJudgment()

    def test01_01_ads_index(self):
        """case01-01 : 首页-已启用的全部banner列表
            不传参数，默认数量为5 """
        api = "/api/v1/ads/index"
        res = self.run_method.get(api)
        res_dict = res.json()
        now_time = int(time.time())
        sql = '''SELECT ad_name FROM `zyt_advertisement` where ad_status =1 and ad_endtime > {};'''.format(
            now_time)
        ad_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.opera_assert.is_equal_value_len(len(res_dict["data"]), 5, ad_num)
