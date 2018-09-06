'''
2018-9-3
广告类接口
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from base.public_param import PublicParam
import unittest


class TestAdvertisement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.run_method = BaseMethod()
        cls.opera_db = OperationDB()
        cls.pub_param = PublicParam()

    def test01_index(self):
        '''首页-已启用的全部banner列表'''
        api = "/api/v1/ads/index"
        res = self.run_method.get(api)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
