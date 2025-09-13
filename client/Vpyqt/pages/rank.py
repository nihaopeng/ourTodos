
from PySide6.QtWidgets import (
    QMessageBox,QPushButton
)
from core.config import getConfig
from core.rank import RankManager
from uipy.rankForm import Ui_Form as RankFormUI
from uipy.loadingForm import Ui_Form as LoadingFormUI
from pages.page import Page, run_in_thread

class RankPage(Page):
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

        # # 加载数据
        # self.loadingUi.show()
        # self.loadRank()
        # self.loadingUi.hide()

        # 连接信号与槽
        self.ui.back2homeBtn.clicked.connect(self.go_to_home)

    def go_to_home(self):
        """跳转到注册页面"""
        # print("跳转到注册页面")
        self.parent_window.switch_to_page("todoList", "left")

    def onSucLoadRank(self,result):
        self.loadingUi.hide()
        self.clear_layout()
        config = getConfig()
        for i,user in enumerate(result):
            userBtn = QPushButton(f"{user["username"]} / score:{user["score"]}")
            if user["username"] == config["USER"]["USERNAME"]:
                userBtn.setStyleSheet("background-color:red;")
                self.ui.rankLabel.setText(f"rank:{i+1}")
            self.ui.verticalLayout.insertWidget(self.ui.verticalLayout.count()-1,userBtn)
        self.loadingUi.hide()

    def loadRank(self):
        if getConfig()["USER"]["EMAIL"]=="":
            return
        # 从远端加载排名数据
        self.loadingUi.show()
        @run_in_thread(on_success=self.onSucLoadRank,on_error=lambda e:(self.loadingUi.hide(),QMessageBox.information(self,"错误",e)))
        def task():
            return self.rankManager.getRank()
        task()

    def clear_layout(self):
        # 减一避免删除掉布局的控件widget
        for i in reversed(range(self.ui.verticalLayout.count()-1)):
            item = self.ui.verticalLayout.itemAt(i)
            if item is None:
                continue
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
                # self.ui.verticalLayout.removeItem(item)
                
    def fresh(self):
        """刷新排名"""
        self.loadRank()
        