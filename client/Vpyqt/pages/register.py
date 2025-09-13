import time
from PySide6.QtWidgets import (
    QWidget, 
    QMessageBox
)
from PySide6.QtCore import QTimer
import requests
from core.config import getConfig
from core.user import UserManager
from uipy.registerForm import Ui_Form as RegisterFormUI
from uipy.loadingForm import Ui_Form as LoadingFormUI
from pages.page import Page

class RegisterPage(Page):
    """注册页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.userManager = UserManager()
        self.req = requests.session()
        
        # 设置UI
        self.loadingUi = LoadingFormUI(self)
        self.ui = RegisterFormUI()
        self.ui.setupUi(self)
        
        # 连接信号
        self.ui.sendCodeBtn.clicked.connect(self.sendCode)
        self.ui.registerBtn.clicked.connect(self.attempt_register)
        self.ui.back2loginBtn.clicked.connect(self.go_to_login)
        # self.ui..clicked.connect(self.go_to_login)

    def sendCode(self):
        self.loadingUi.show()
        email = self.ui.emailLineEdit.text()
        if email:
            QTimer.singleShot(0, lambda: self.sendCodeTask(email))
            self.ui.sendCodeBtn.setEnabled(False)
        else:
            QMessageBox.warning(self, "错误","请先填写邮箱")
    
    def sendCodeTask(self,email):
        # status,reason = self.userManager.sendCode(email)
        time.sleep(2)  # 模拟网络延迟
        status,reason = True,""
        if status:
            QMessageBox.information(self, "发送成功", f"验证码已发送至 {email}，请注意查收！")
            # 启动60秒倒计时
            # self.countdown(60)
            self.loadingUi.hide()
        else:
            QMessageBox.information(self, "发送失败", f"{reason}")
            self.ui.sendCodeBtn.setEnabled(True)
    
    def attempt_register(self):
        """尝试注册"""
        username = self.ui.usernameLineEdit.text()
        email = self.ui.emailLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        code = self.ui.codeLineEdit.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写！")
            return
            
        # 在实际应用中，这里会有注册逻辑
        status,reason = self.userManager.register(email,username,password,code)
        if status:
            QMessageBox.information(self, "注册成功", f"用户 {username} 注册成功！")
        else:
            QMessageBox.information(self, "注册失败", f"{reason}")
        self.go_to_login()
    
    def go_to_login(self):
        """跳转到登录页面"""
        self.parent_window.switch_to_page("login", "right")
        
    def fresh(self):
        return super().fresh()