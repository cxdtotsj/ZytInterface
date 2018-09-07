
import pymysql
import base.setting
import time


class OperationDB:

    def __init__(self):
        self.host = base.setting.DB_HOST
        self.port = base.setting.DB_PORT
        self.user = base.setting.DB_USER
        self.pwd = base.setting.DB_PASSWORD
        self.db_name = base.setting.DB_DB
        self.db = self.get_db()
        self.mycursor = self.get_cursor()

    def get_db(self):
        db = pymysql.connect(host=self.host,
                             port=self.port,
                             user=self.user,
                             password=self.pwd,
                             db=self.db_name,
                             charset="utf8",
                             autocommit=True,
                             cursorclass=pymysql.cursors.DictCursor)
        return db

    def get_cursor(self):
        mycursor = self.db.cursor()
        return mycursor

    # 获取行数
    def get_effect_row(self, sql, paramers=None):
        if paramers is None:
            effect_row = self.mycursor.execute(sql)
        else:
            effect_row = self.mycursor.execute(sql % paramers)
        return effect_row

    # 获取第一个返回结果
    def get_fetchone(self, sql, paramers=None):
        if paramers is None:
            self.mycursor.execute(sql)
        else:
            self.mycursor.execute(sql % paramers)
        row_one = self.mycursor.fetchone()
        return row_one

    # 获取指定返回结果
    def get_fetchmany(self, sql, n, paramers=None):
        if paramers is None:
            self.mycursor.execute(sql)
        else:
            self.mycursor.execute(sql % paramers)
        row_num = self.mycursor.fetchmany(n)
        return row_num

    # 获取全部返回结果
    def get_fetchall(self, sql, paramers=None):
        if paramers is None:
            self.mycursor.execute(sql)
        else:
            self.mycursor.execute(sql % paramers)
        row_all = self.mycursor.fetchall()
        return row_all

    # 更新数据
    def update_data(self, sql):
        try:
            self.mycursor.execute(sql)
            self.db.commit()
        except BaseException:
            self.db.rollback()

    # 插入数据
    def insert_data(self, sql):
        try:
            self.mycursor.execute(sql)
            self.db.commit()
        except BaseException:
            self.db.rollback()

    # 删除数据
    def delete_data(self, sql):
        try:
            self.mycursor.execute(sql)
            self.db.commit()
        except BaseException:
            self.db.rollback()

    # 关闭数据库连接
    def close_db(self):
        self.mycursor.close()


if __name__ == '__main__':
    from data.sql_data import SQLData
    get_data = SQLData()
    dbdata = OperationDB()
    now_time = int(time.time())
    sql = '''SELECT id FROM `zyt_classes` where classes_status = 1 ORDER BY created_time DESC;'''
    new_course = dbdata.get_fetchmany(sql, 1000)
    # value_dict = get_data.array_get_dictValue(new_course,"id")
    # print(value_dict)
    print(new_course)
