from util.operation_db import OperationDB
import random
import time


class SQLData:

    def __init__(self):
        self.opera_db = OperationDB()

    # 自动插入一条 无需报名的活动，并返回出 id
    def insert_event_no(self):
        num = random.randint(1, 100)
        event_title = "这是活动--名称{}".format(num)
        event_intro = "这是活动--说明{}".format(num)
        event_content = "这是活动--内容{}".format(num)
        created_time = int(time.time())
        noAllow_sql = '''insert into zyt_event (event_title,event_intro,event_content,apply_need,end_time,event_rank,event_status,created_time,created_user)
                            value ("{}","{}","{}",0,{},0,1,{},"xdchen")'''.format(event_title, event_intro, event_content, created_time, created_time)
        self.opera_db.insert_data(noAllow_sql)
        noAllowID_sql = '''select id from zyt_event where event_title = '{}' ORDER BY created_time DESC'''.format(
            event_title)
        no_eventID = self.opera_db.get_fetchone(noAllowID_sql)["id"]
        return no_eventID

    # 需要报名的活动，并返回出 id
    def insert_event_yes(self):
        num = random.randint(1, 100)
        event_title = "这是报名活动--名称{}".format(num)
        event_intro = "这是报名活动--说明{}".format(num)
        event_content = "这是报名活动--内容{}".format(num)
        created_time = int(time.time())
        end_time = int(time.time() + 1000)
        yesAllow_sql = '''insert into zyt_event (event_title,event_intro,event_content,apply_need,allowed_num,end_time,event_rank,event_status,created_time,created_user)
                            value ("{}","{}","{}",1,5,{},0,1,{},"xdchen")'''.format(event_title, event_intro, event_content, end_time, created_time)
        self.opera_db.insert_data(yesAllow_sql)
        yseAllowID_sql = '''select id from zyt_event where event_title = '{}' ORDER BY created_time DESC'''.format(
            event_title)
        yse_eventID = self.opera_db.get_fetchone(yseAllowID_sql)["id"]
        return yse_eventID

    # 获取数据库或者返回值发返出的数据，把value放入列表
    def array_get_dictValue(self, array, key):
        value_list = []
        for i in array:
            value_list.append(i[key])
        return value_list


if __name__ == "__main__":
    sql = SQLData()
    id = sql.insert_event_yes()
    print(id)
