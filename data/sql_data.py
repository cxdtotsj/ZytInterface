from util.operation_db import OperationDB

class SQLData:

    def __init__(self):
        self.opera_db = OperationDB()

    # 自动插入一条 无需报名的活动，并返回出 id
    def insert_eventNo(self):
        noAllow_sql = '''insert into zyt_event (event_title,event_intro,event_content,apply_need,event_rank,event_status) value ("test01","test02","test03",0,0,1)'''
        self.opera_db.insert_data(noAllow_sql)
        noAllowID_sql = '''select id from zyt_event where event_title = 'test01' ORDER BY created_time DESC'''
        no_eventID = self.opera_db.get_fetchone(noAllowID_sql)["id"]
        return no_eventID
    #
    # # 需要报名的活动，并返回出 id
    # def insert_eventYes(self):
    #     yesAllow_sql =

# if __name__ == "__main__":
