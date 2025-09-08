
from PySide6.QtWidgets import (
    QWidget,QPushButton
)
from core.rank import RankManager
from uipy.rankForm import Ui_Form as RankFormUI
from uipy.loadingForm import Ui_Form as LoadingFormUI

class RankPage(QWidget):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        self.rankManager = RankManager()
        
        # 设置UI
        self.ui = RankFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFormUI(self)

        # 加载数据
        self.loadingUi.show()
        self.loadRank()
        self.loadingUi.hide()

        # 连接信号与槽
        self.ui.back2homeBtn.clicked.connect(self.go_to_home)

    def go_to_home(self):
        """跳转到注册页面"""
        # print("跳转到注册页面")
        self.parent_window.switch_to_page("todoList", "left")

    def loadRank(self):
        # 从远端加载排名数据
        rank = self.rankManager.getRank()
        self.clear_layout()
        for user in rank:
            userBtn = QPushButton(f"{user["username"]} / {user["score"]}")
            self.ui.verticalLayout.insertWidget(self.ui.verticalLayout.count()-1,userBtn)

    def clear_layout(self):
        # 减一避免删除掉布局的控件widget
        for i in reversed(range(self.ui.verticalLayout.count()-1)):
            widget = self.ui.verticalLayout.itemAt(i).widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()