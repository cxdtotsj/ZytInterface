
import pymysql
import base.setting


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
    dbdata = OperationDB()
    paramers = (1, 0, 1)
    sql = '''update zyt_user_like set type =1 where id = 50;'''
    a = dbdata.update_data(sql)
    print(a)
