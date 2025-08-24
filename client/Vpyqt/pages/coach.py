
from PySide6.QtWidgets import (
    QWidget,QPushButton
)
from backend.LLMCaller import LLMCaller
from backend.provider import deepseek
from uipy.coachForm import Ui_Form as CoachFormUI
from uipy.loadingForm import Ui_Form as LoadingFormUI
from PySide6.QtCore import QObject, QThread, Signal

class LLMWorker(QObject):
    chunk_signal = Signal(str)   # 每次接收到的分块
    start_signal = Signal()
    finished = Signal()          # 完成信号

    def __init__(self, llmcaller, query):
        super().__init__()
        self.llmcaller = llmcaller
        self.query = query

    def run(self):
        fulltext = ""
        for chunk in self.llmcaller.stream(self.query):
            fulltext += chunk
            self.start_signal.emit()
            self.chunk_signal.emit(fulltext)  # 把最新文本发给UI
        self.finished.emit()

class CoachPage(QWidget):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        
        # 设置UI
        self.ui = CoachFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFormUI(self)

        # 连接信号与槽
        self.ui.back2homeBtn.clicked.connect(self.go_to_home)
        self.ui.callCoachBtn.clicked.connect(self.start_coaching)

        # 逻辑处理
        self.LLMCaller = LLMCaller()  # 假设你有一个 LLMCaller 类来处理模型调用
        self.LLMCaller.register_model("deepseek", deepseek.handler_factory)
    
    def go_to_home(self):
        """跳转到注册页面"""
        # print("跳转到注册页面")
        self.parent_window.switch_to_page("todoList", "left")

    def start_coaching(self):
        task = self.ui.taskLineEdit.text()
        if not task.strip():
            return
        
        TEMPLATE = """
        现在有一个用户的任务，但是处于某些原因，用户没有动力完成这个任务。
        你需要充当一个教练，根据用户现在所处的状态，帮助用户完成这个任务。
        请将任务分解为多个步骤
        每个步骤只需要一个序号加一句话,只输出步骤
        注意重点是如何启动这个任务，而不是如何完成这个任务，比如：我说我现在躺在床上玩手机，想去自习室学习
        你可以提出
        1、起身，离开床铺
        2、穿鞋
        3、带上学习用品
        4、前往自习室
        可以细致一些，不要太宽泛。

        任务如下：
        <task>
        {task}
        </task>
        """.format(task=task)

        # 清空旧内容
        self.ui.textBrowser.clear()
        #加载动画
        self.loadingUi.show()

        # 创建 worker + 线程
        self.thread = QThread()
        self.worker = LLMWorker(self.LLMCaller, TEMPLATE)
        self.worker.moveToThread(self.thread)

        # 连接信号
        self.thread.started.connect(self.worker.run)
        self.worker.chunk_signal.connect(self.update_text)
        self.worker.start_signal.connect(self.start_gen)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        # 启动线程
        self.thread.start()

    def update_text(self, text):
        """实时更新到 textBrowser"""
        self.ui.textBrowser.setText(text)

    def start_gen(self):
        # 开始生成，关闭加载动画
        self.loadingUi.hide()