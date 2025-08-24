
from PySide6.QtWidgets import (
    QWidget
)
from uipy.rankForm import Ui_Form as RankFormUI
from uipy.loadingForm import Ui_Form as LoadingFormUI

class RankPage(QWidget):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        
        # 设置UI
        self.ui = RankFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFormUI(self)

        # 加载数据
        self.loadingUi.show()
        # TODO:加载数据
        self.loadingUi.hide()
        # TODO:显示排名

        # 连接信号与槽
        self.ui.back2homeBtn.clicked.connect(self.go_to_home)

    def go_to_home(self):
        """跳转到注册页面"""
        # print("跳转到注册页面")
        self.parent_window.switch_to_page("todoList", "left")

    def loadRank(self):
        # 从远端加载排名数据
        pass