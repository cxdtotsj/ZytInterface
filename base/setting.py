
# 项目名称
ENV = "Proto Testing"

# GRPC参数和方法名
gprc_base_url = "{0[0]} -plaintext -d '%s' -import-path {0[1]} -proto %s"

# GRPC命令及proto文件地址
grpc_base_params = ["/home/bear/go/src/pb/grpcurl", "/home/bear/go/src/pb/"]


# 拼接grpc_base_url
grpc_format_url = gprc_base_url.format(grpc_base_params)


# HTTP地址常量
http_base_url = "https://zyt-dev.arctron.cn"

# 数据库信息
DB_HOST = "newhero.mysqldb.chinacloudapi.cn"
DB_PORT = 3306
DB_USER = "newhero%herouser"
DB_PASSWORD = "hero123!@#"
DB_DB = "hero"

if __name__ == '__main__':
    import pymysql
    my_con = pymysql.connect(host="newhero.mysqldb.chinacloudapi.cn",
                             port=3306,
                             user='newhero%herouser',
                             passwd='hero123!@#',
                             db='hero',
                             charset='utf8'
                             )
    my_cousor = my_con.cursor()
    # 获取数据库游标对象
    sql_select = 'select * from zyt_classes where is_top =%d  and set_rank != %d  and classes_status=%d ORDER BY set_rank;'
    paramers = (1, 0, 1)
    # 用一个变量接收mysql语句
    my_cousor.execute(sql_select % paramers)
    # 执行
    my_cousor.rowcount
    # 返回被execute影响的数据的行数,注：execute不是方法.
    get_row = my_cousor.fetchone()
    # 取结果集下一行
    print(get_row)
    get_row = my_cousor.fetchmany(3)
    # 取结果集下三行
    print(get_row)
    get_row = my_cousor.fetchall()
    # 取结果集剩下所有行
    print(get_row)

    my_cousor.close()
    # 关闭游标
    my_con.close()
