
from PySide6.QtWidgets import (
    QWidget,QCheckBox,QPushButton,QHBoxLayout,QMessageBox
)
from pages.page import Page
from core.coach import CoachManager, Step
from uipy.coachForm import Ui_Form as CoachFormUI
from uipy.loadingForm import Ui_Form as LoadingFormUI

class StepCheckBox(QCheckBox):
    def __init__(self,step:Step,parent=None):
        super().__init__(step.stepName,parent)
        self.step = step

class StepWidget(QWidget):
    def __init__(self,stepCheckBox:StepCheckBox,parent):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 去掉边距

        self.stepCheckBox = stepCheckBox
        self.delete_btn = QPushButton("❌", self)
        self.delete_btn.setFixedSize(24, 24)

        layout.addWidget(self.stepCheckBox)
        layout.addWidget(self.delete_btn)

        # 点击删除按钮时，删除自己
        self.delete_btn.clicked.connect(self.delete_self)
    
    def delete_self(self):
        # 从父布局移除并销毁自己
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            parent_layout.removeWidget(self)
        self.deleteLater()

class CoachPage(Page):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        self.coachManager = CoachManager()
        # 设置UI
        self.ui = CoachFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFormUI(self)

        # 连接信号与槽
        self.ui.back2homeBtn.clicked.connect(self.gotoHome)
        self.ui.callCoachBtn.clicked.connect(self.startCoaching)
        self.coachManager.startSignal.connect(self.loadingUi.hide)# 开始生成内容，关闭加载动画
        self.coachManager.stepSignal.connect(self.updateText)
        self.coachManager.errorSignal.connect(lambda v:QMessageBox.information(self,"错误",v))
    
    def gotoHome(self):
        """跳转到注册页面"""
        # print("跳转到注册页面")
        self.parent_window.switch_to_page("todoList", "left")

    def startCoaching(self):
        task = self.ui.taskLineEdit.text()
        self.coachManager.genStep(task)
        self.loadingUi.show()

    def updateText(self, step:Step):
        """实时更新到 textBrowser"""
        stepCheckBox = StepCheckBox(step,self)
        stepWidget = StepWidget(stepCheckBox,self)
        self.ui.verticalLayout_2.insertWidget(self.ui.verticalLayout_2.count()-1,stepWidget)
        
    def fresh(self):
        return super().fresh()