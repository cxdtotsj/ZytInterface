import os


# 项目名称
ENV = "Proto Testing"

# GRPC参数和方法名
gprc_base_url = "{} -plaintext -d '%s' -import-path {} -proto %s"

# GRPC命令及proto文件地址
grpc = "/home/bear/go/src/pb/grpcurl"
proto_file = "/home/bear/go/src/pb/"
# grpc_base_params = ["/home/bear/go/src/pb/grpcurl", "/home/bear/go/src/pb/"]

# 拼接grpc_base_url
grpc_format_url = gprc_base_url.format(grpc, proto_file)


# HTTP域名
http_base_url = "https://zyt-dev.arctron.cn"

# 数据库信息
DB_HOST = "newhero.mysqldb.chinacloudapi.cn"
DB_PORT = 3306
DB_USER = "newhero%herouser"
DB_PASSWORD = "hero123!@#"
DB_DB = "hero"

if __name__ == '__main__':
    print(grpc_format_url)