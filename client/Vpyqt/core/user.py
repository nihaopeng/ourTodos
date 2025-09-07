import requests

from core.config import getConfig, setConfig


class UserManager():
    def __init__(self) -> None:
        self.req = requests.session()

    def login(self,email,password):
        data = {
            "email":email,
            "password":password
        }
        res = self.req.post(f"{getConfig()["REMOTE"]["URL"]}/login",json=data)
        res = res.json()
        if res["code"]==200:
            config = getConfig()
            config["USER"]["USERNAME"] = res["username"]
            config["USER"]["EMAIL"] = email
            config["USER"]["PASSWORD"] = password
            setConfig(config)
            return res["username"]
        else:
            return None

    def register(self,email,username,password,code):
        data = {
            "email":email,
            "username":username,
            "password":password,
            "code":code
        }
        res = self.req.post(f"{getConfig()["REMOTE"]["URL"]}/regist",json=data)
        res = res.json()
        if res["code"]==200:
            return True,res["msg"]
        else:
            return False,res["msg"]
        
    def sendCode(self,email):
        data = {
            "email":email
        }
        res = self.req.post(f"{getConfig()["REMOTE"]["URL"]}/send_verification_code",json=data)
        res = res.json()
        if res["code"]==200:
            return True,res["msg"]
        else:
            return False,res["msg"]