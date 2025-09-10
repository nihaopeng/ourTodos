import uuid
from core.config import getConfig, setConfig,request
import uuid
from core.LLMCaller import LLMCaller
from core.provider import deepseek
from PySide6.QtCore import QObject, Signal, Slot, QThread,QDate

class RankManager(QObject):
    def __init__(self) -> None:
        super().__init__()
    
    def getScores(self):
        email = getConfig()["USER"]["EMAIL"]
        if email=="":
            pass
        else:
            data = {
                "email":getConfig()["USER"]["EMAIL"]
            }
            res = request("get_scores",json=data)
            res = res.json()
            if res["code"]==200:
                return res["data"]
            else:
                return None

    def getRank(self):
        Scores = self.getScores()
        # print(Scores)
        rank = sorted(Scores, key=lambda x: x["score"], reverse=True)
        # print(rank)
        return rank