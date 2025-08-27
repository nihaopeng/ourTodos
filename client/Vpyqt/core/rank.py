import uuid
from core.config import getConfig, setConfig
import uuid
from core.LLMCaller import LLMCaller
from core.provider import deepseek
from PySide6.QtCore import QObject, Signal, Slot, QThread,QDate

class RankManager(QObject):
    def __init__(self) -> None:
        super().__init__()
    
    def getScores(self):
        pass

    def genRank(self):
        pass