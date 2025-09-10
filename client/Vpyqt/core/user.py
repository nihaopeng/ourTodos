import requests

from core.config import getConfig, setConfig,request

class UserManager():

    def login(self,email,password):
        data = {
            "email":email,
            "password":password
        }
        res = request("login",json=data)
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
        res = request("regist",json=data)
        res = res.json()
        if res["code"]==200:
            return True,res["msg"]
        else:
            return False,res["msg"]
        
    def sendCode(self,email):
        data = {
            "email":email
        }
        res = request("send_verification_code",json=data)
        res = res.json()
        if res["code"]==200:
            return True,res["msg"]
        else:
            return False,res["msg"]
        
    def getScore(self):
        config = getConfig()
        email = config["USER"]["EMAIL"]
        if email=="":
            return True,config["USER"]["SCORE"]
        else:
            data = {
                "email":email
            }
            res = request("get_user_score",json=data)
            res = res.json()
            # print(res)
            if res["code"]==200:
                return True,str(res["score"])
            else:
                return False,res["msg"]