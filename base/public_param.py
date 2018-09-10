from base.baseMethod import BaseMethod
from util.operation_db import OperationDB


class PublicParam:

    def __init__(self):
        self.run_method = BaseMethod()
        self.opera_db = OperationDB()
        self.token = self.get_token()[0]
        self.user_id = self.get_token()[1]

    def get_token(self):
        api = "/api/v1/user/login"
        data = {"mobile": 18321829313, "password": "Password02!"}
        res = self.run_method.post(api, data)
        if res.status_code == 200:
            res_dict = res.json()
            try:
                self.token = res_dict["data"]["token"]
                self.user_id = res_dict["data"]["user_id"]
                return self.token, self.user_id
            except BaseException:
                print("用户名或验证码错误")
        else:
            print("服务器登陆失败")

    def test_token(self):
        api = "/api/v1/course/detail/1"
        data = {"token": self.token, "user_id": self.user_id}
        res = self.run_method.get(api, data).json()
        return res


if __name__ == "__main__":
    import time
    basedata = PublicParam()
    token = basedata.get_token()[0]
    print(token)
    print("\n")
    time.sleep(3)
    data1 = basedata.testtoken()
    print(data1["data"]["token"])
