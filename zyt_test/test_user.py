'''
2018-9-3
用户类接口
用户user_id : d5eba536a06411e8b6e30017fa004b58
问题点赞id : 254
'''

from base.baseMethod import BaseMethod
from util.operation_db import OperationDB
from base.public_param import PublicParam
import datetime
import random
import unittest


class TestUser(unittest.TestCase):

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

    def test01_SaveProject(self):
        '''新增作品'''

        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        api = "/api/v1/user/saveproject"
        data = {"user_id": self.user_id,
                "token": self.token,
                "p_name": "作品名称 %s" % (time_now),
                "p_desc": "作品简介 %s" % (time_now),
                "p_img": "/1535965522439599110?imageView2/2/w/212/h/136/q/100"}
        res = self.run_method.post(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_project where user_id = '{}' ORDER BY created_at DESC;'''.format(
            self.user_id)
        new_project = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["last_id"],
            new_project["id"],
            "最新作品返回不正确")

    def test02_Follow(self):
        '''关注或取消关注某用户'''

        api = "/api/v1/user/follow"
        follow_usr_id = "f350756baf4211e8b6e30017fa004b58"
        sql = '''select attention_user_id from zyt_user_attention where user_id = '{}' and attention_user_id = '{}';'''.format(
            self.user_id, follow_usr_id)
        before_follow = self.opera_db.get_fetchone(sql)
        if before_follow:
            data = {
                "follow_user_id": follow_usr_id,
                "t": "cancel",
                "user_id": self.user_id,
                "token": self.token}
        else:
            data = {
                "follow_user_id": follow_usr_id,
                "t": "add",
                "user_id": self.user_id,
                "token": self.token}
        res = self.run_method.post(api, data)
        update_follow = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        if before_follow:
            self.assertIsNone(update_follow, "取消关注用户失败")
        else:
            self.assertEqual(
                update_follow["attention_user_id"],
                follow_usr_id,
                "关注用户失败")

    def test03_EditDefault(self):
        '''编辑个人资料'''

        api = "/api/v1/user/edit"
        nick_name = "bear%s" % (random.randint(1, 50))
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "default",
            "savedata": {
                "nickname": nick_name,
                "name": "bear chen",
                "skill_id": 1,
                "cert": [],
                "avatar": "/1534730680812962881?imageView2/2/w/356/h/356/q/100",
                "company": "公司--华建数创",
                "company_position": "",
                "social_position": ["职位--测试|undefined"],
                "expertise": [],
                "email": "",
                "description": "",
                "phone": "18321829313"}}
        headers = {"content-type": "application/json"}
        res = self.run_method.post(api, data, headers=headers)
        sql = '''select nickname from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        update_nickname = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(update_nickname["nickname"], nick_name, "昵称未更新成功")

    def test04_EditVerify(self):
        '''
        申请专家认证，
        暂时不清楚可以进行多少次专家认证，暂时不写具体逻辑
        '''
        pass

    def test05_MyOpenQa(self):
        '''开启专家咨询，设置价格'''

        api = "/api/v1/user/myopenqa"
        sql = '''select is_open_ask,ask_price from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        before_myopenqa = self.opera_db.get_fetchone(sql)
        price = random.randint(0, 5)
        if before_myopenqa["is_open_ask"] == 0:
            data = {"user_id": self.user_id,
                    "token": self.token,
                    "type": "open",
                    "price": price}
        else:
            data = {"user_id": self.user_id,
                    "token": self.token,
                    "type": "close"}
        res = self.run_method.post(api, data)
        update_myopenqa = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        if before_myopenqa["is_open_ask"] == 0:
            self.assertEqual(update_myopenqa["is_open_ask"], 1, "开启提问未设置成功")
            self.assertEqual(update_myopenqa["ask_price"], price, "提问价格未更新成功")
        else:
            self.assertEqual(update_myopenqa["is_open_ask"], 0, "关闭提问未设置成功")

    def test06_FeedBack(self):
        '''用户反馈'''

        api = "/api/v1/user/feedback"
        feed_content = "自动反馈内容 %s" % (
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        data = {"user_id": self.user_id,
                "token": self.token,
                "feed_content": feed_content}
        res = self.run_method.post(api, data)
        sql = '''select content from zyt_user_feedback where user_id = '{}' ORDER BY created_at desc;'''.format(
            self.user_id)
        new_content = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        self.assertEqual(new_content["content"], feed_content, "反馈内容未提交")

    def test07_Like(self):
        '''点赞或取消赞'''

        api = "/api/v1/user/likes"
        sql = '''select relation_id from zyt_user_like where user_id = '{}' and relation_id = 254;'''.format(
            self.user_id)
        before_act = self.opera_db.get_fetchone(sql)
        if before_act:
            data = {"user_id": self.user_id,
                    "token": self.token,
                    "relation_id": 254,
                    "type": 1,
                    "act": "cancel"}
        else:
            data = {"user_id": self.user_id,
                    "token": self.token,
                    "relation_id": 254,
                    "type": 1,
                    "act": "add"}
        res = self.run_method.post(api, data)
        update_act = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res.json())
        if before_act:
            self.assertIsNone(update_act, "未成功取消点赞")
        else:
            self.assertEqual(update_act["relation_id"], 254, "点赞未成功")

    def test08_MyCourseBuy(self):
        '''我的课程--购买'''

        api = "/api/v1/user/mycourse"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": 1,
                "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select classes_id from zyt_user_classes where user_id = '{}' and status = 1;'''.format(
            self.user_id)
        course_buy = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if course_buy >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的已购买课程数量不正确")
        elif 1 <= course_buy < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的购买课程数量不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "没有购买的课程")

    def test09_MyCourseCollection(self):
        '''我的课程--收藏'''

        api = "/api/v1/user/mycourse"
        data = {"user_id": self.user_id,
                "token": self.token,
                "t": 1,
                "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select classes_id from zyt_user_classes where user_id = '{}' and status = 2;'''.format(
            self.user_id)
        course_collection = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if course_collection >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的已收藏课程数量不正确")
        elif 1 <= course_collection < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的已收藏课程数量不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "没有收藏的课程")

    def test10_MyQuestionAsk(self):
        '''我的问题--提问'''

        api = "/api/v1/user/myquestion"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "ask",
            "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where user_id = '{}' and ask_status in (0,1,2,5);'''.format(
            self.user_id)
        question_ask = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if question_ask >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的我问的问题数不正确")
        elif 1 <= question_ask < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的我问的问题数不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "不存在我问的问题")

    def test11_MyQuestionBuy(self):
        '''我的问题--购买问题'''

        api = "/api/v1/user/myquestion"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "buy",
            "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select ask_id from zyt_user_buy_ask where user_id = '{}';'''.format(
            self.user_id)
        question_buy = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if question_buy >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的购买答案数不正确")
        elif 1 <= question_buy < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回购买答案数不正确")
        else:
            print(len(res_dict["data"]["data"]))
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "不存在购买的答案")

    def test12_MyQuestionClose(self):
        '''我的问题--关闭的问题'''

        api = "/api/v1/user/myquestion"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "close",
            "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where user_id = '{}' and ask_status in (3,4);'''.format(
            self.user_id)
        question_close = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if question_close >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的关闭的问题数不正确")
        elif 1 <= question_close < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的关闭的问题数不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "不存在关闭的问题")

    def test13_MyAnswerWait(self):
        '''我的待回答问题'''

        api = "/api/v1/user/myanswer"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "wait",
            "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_ask where answer_user_id = '{}' and ask_status = 0;'''.format(
            self.user_id)
        answer_wait = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if answer_wait >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的待回答问题数不正确")
        elif 1 <= answer_wait < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的待回答问题数不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "不存在待回答问题")

    def test14_MyAnswerDone(self):
        '''我的已回答问题'''

        api = "/api/v1/user/myanswer"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "done",
            "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select ask_id from zyt_user_answer where user_id = '{}';'''.format(
            self.user_id)
        answer_done = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if answer_done >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的已回答问题数不正确")
        elif 1 <= answer_done < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的已回答问题数不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "不存在已回答问题")

    def test15_MyQuesionAppeal(self):
        '''对专家回答进行申诉，流程性用例'''
        pass

    def test16_UserDetail(self):
        '''用户详情'''

        api = "/api/v1/user/detail/{}".format(self.user_id)
        data = {"user_id": self.user_id,
                "token": self.token}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select phone from zyt_user where user_id = '{}';'''.format(
            self.user_id)
        user_phone = self.opera_db.get_fetchone(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        self.assertEqual(
            res_dict["data"]["user_id"],
            data["user_id"],
            "返回的user_id不正确")
        self.assertEqual(
            res_dict["data"]["phone"],
            user_phone["phone"],
            "用户手机号返回不正确")

    def test17_ProjectList(self):
        '''用户作品'''

        api = "/api/v1/user/projectlist/{}".format(self.user_id)
        data = {"l": 6}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_project where user_id = '{}';'''.format(
            self.user_id)
        product_list = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if product_list >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的作品数不正确")
        elif 1 <= product_list < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的作品数不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "不存在作品")

    def test18_MyMessage(self):
        '''我的站内消息（带翻页）'''

        api = "/api/v1/user/mymessage"
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "done",
            "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select id from zyt_user_message where user_id = '{}';'''.format(
            self.user_id)
        message_num = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if message_num >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["list"]["data"]), data["l"], "返回的消息数不正确")
        elif 1 <= message_num < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["list"]["data"]) < data["l"],
                "返回的消息数不正确")
        else:
            self.assertTrue(
                len(res_dict["data"]["list"]["data"]) == 0, "不存在消息")

    def test19_DynamicList(self):
        '''用户动态列表(带翻页)'''

        api = "/api/v1/user/dynamiclist/{}".format(self.user_id)
        data = {
            "user_id": self.user_id,
            "token": self.token,
            "t": "done",
            "l": 10}
        res = self.run_method.get(api, data)
        res_dict = res.json()
        sql = '''select * from zyt_user_dynamics where user_id = '{}' ORDER BY created_at DESC;'''.format(
            self.user_id)
        dynamic_list = self.opera_db.get_effect_row(sql)

        self.assertEqual(res.status_code, 200, "HTTP状态码不为200")
        self.assertEqual(
            self.run_method.get_result(res),
            "success", res_dict)
        if dynamic_list >= data["l"]:
            self.assertEqual(
                len(res_dict["data"]["data"]), data["l"], "返回的动态数不正确")
        elif 1 <= dynamic_list < data["l"]:
            self.assertTrue(
                1 <= len(
                    res_dict["data"]["data"]) < data["l"],
                "返回的动态数不正确")
        else:
            self.assertTrue(len(res_dict["data"]["data"]) == 0, "不存在动态")
