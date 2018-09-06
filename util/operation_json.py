import json

class OperetionJson:

    def __init__(self,file_path=None):
        if file_path == None:
            self.file_path = '../dataconfig/test_data.json'
        else:
            self.file_path = file_path
        self.data = self.read_data()

    # 读取json文件
    def read_data(self):
        with open(self.file_path) as fp:
            data = json.load(fp)
            return data

    # 根据关键字获取数据
    def get_data(self,id):
        return self.data[id]

    # 写json
    def write_data(self,data):
        with open(self.file_path,'w') as fp:
            fp.write(json.dumps(data))
            fp.close()

    # 重写json
    def check_json_value(self,depend_key,depend_vaule):
        json_data = self.data
        json_data[depend_key] = depend_vaule
        self.write_data(json_data)


if __name__ == "__main__":
    file = '../dataconfig/zyt_data.json'
    opera_json = OperetionJson(file)
    data = {"user_id":123,"token":"abc"}
    opera_json.check_json_value("test02",data)
    user_id = opera_json.get_data("test02")["user_id"]
    print(user_id)
