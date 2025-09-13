from PySide6.QtWidgets import (
    QMessageBox
)
from PySide6.QtCore import QTimer
from pages.page import run_in_thread
import requests
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
    
    def countdown(self, seconds=60):
        self.remaining_time = seconds
        self.ui.sendCodeBtn.setText(f"{self.remaining_time}s")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateCountdown)
        self.timer.start(1000)  # 每秒触发一次
    
    def updateCountdown(self):
        self.remaining_time -= 1
        if self.remaining_time > 0:
            self.ui.sendCodeBtn.setText(f"{self.remaining_time}s")
        else:
            self.timer.stop()
            self.ui.sendCodeBtn.setEnabled(True)
            self.ui.sendCodeBtn.setText("发送验证码")

    def sendCode(self):
        # self.loadingUi.show()
        email = self.ui.emailLineEdit.text()
        if email:
            self.countdown(60)  # 启动倒计时
            @run_in_thread(on_success=self.onSucSendCode,on_error=None)
            def task(email):
                return self.userManager.sendCode(email)
            task(email)
        else:
            QMessageBox.warning(self, "错误","请先填写邮箱")

    def onSucSendCode(self, result):
        # print(result)
        status, reason = result[0], result[1]
        if status:
            QMessageBox.information(self, "发送成功", "验证码已发送，请注意查收！")
        else:
            QMessageBox.information(self, "发送失败", reason)
            self.timer.stop()
            self.ui.sendCodeBtn.setEnabled(True)
            self.ui.sendCodeBtn.setText("发送验证码")

    def onSucRegister(self, result):
        status, reason = result[0], result[1]
        if status:
            QMessageBox.information(self, "注册成功", "注册成功，请登录！")
            self.loadingUi.hide()
            self.go_to_login()
        else:
            QMessageBox.information(self, "注册失败", reason)
            self.loadingUi.hide()
    
    def attempt_register(self):
        """尝试注册"""
        username = self.ui.usernameLineEdit.text()
        email = self.ui.emailLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        code = self.ui.codeLineEdit.text()
        
        if not username or not email or not password or not code:
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写！")
            return
        self.loadingUi.show()
        @run_in_thread(on_success=self.onSucRegister,on_error=None)
        def task(email,username,password,code):
            return self.userManager.register(email,username,password,code)
        task(email,username,password,code)

    def go_to_login(self):
        """跳转到登录页面"""
        self.parent_window.switch_to_page("login", "right")
        
    def fresh(self):
        return super().fresh()