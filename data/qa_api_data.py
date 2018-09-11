"""
1.test_qa 测试文件的继承
"""
import datetime
from base.public_param import PublicParam
from util.operation_json import OperetionJson
from base.baseMethod import BaseMethod
from base.getURL import API


class QaApiData:

    def __init__(self):
        self.opera_json = OperetionJson()
        self.get_url = API()
        self.run_method = BaseMethod()

    # 专家提问接口 /api/v1/qa/qsubmit
    qa_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    qa_title = "这是问题题目 -- %s" % qa_time
    qa_desc = "这是问题描述 -- %s" % qa_time
    qa_img_one = ["/1536116758846885506?imageView2/2/w/212/h/136/q/100"]
    qa_img_four = ["/1536116758846885506?imageView2/2/w/212/h/136/q/100",
                  "/1536116758846885506?imageView2/2/w/212/h/136/q/100",
                  "/1536116758846885506?imageView2/2/w/212/h/136/q/100",
                  "/1536116758846885506?imageView2/2/w/212/h/136/q/100"]
    qa_headers = {"content-type": "application/json"}

    # 专家回答接口 /api/v1/qa/asubmit
    answer_content = "这是问题答案 -- %s" % qa_time

