
from PySide6.QtWidgets import (
    QWidget,QMessageBox
)
from pages.page import Page
from core.config import getConfig,setConfig
from core.user import UserManager
from pages.settings import SettingsPage
from pages.todoList import TodoListPage
from uipy.loginForm import Ui_Form as LoginFormUI

class LoginPage(Page):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        self.userManager = UserManager()
        # 设置UI
        self.ui = LoginFormUI()
        self.ui.setupUi(self)
        self.ui.emailLineEdit.setText(getConfig()["USER"]["EMAIL"])
        self.ui.passwordLineEdit.setText(getConfig()["USER"]["PASSWORD"])

        # 连接信号与槽
        self.ui.loginConfirmBtn.clicked.connect(self.attempt_login)
        self.ui.registerBtn.clicked.connect(self.go_to_register)
        self.ui.customerLoginBtn.clicked.connect(self.customLogin)
    
    def attempt_login(self):
        """尝试登录"""
        email = self.ui.emailLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        
        if not email or not password:
            QMessageBox.warning(self, "输入错误", "用户名和密码不能为空！")
            # messageBox("输入错误", "用户名和密码不能为空！",self)
            return
            
        # 在实际应用中，这里会有身份验证逻辑
        username = self.userManager.login(email,password)
        if username:
            # self.parent_window.register_page("todoList", TodoListPage(self.parent_window))
            # QMessageBox.critical(self, "登录", "")
            self.parent_window.switch_to_page("todoList", "right")
            self.parent_window.show_desktop()
            self.parent_window.set_desktop_window()
        else:
            QMessageBox.critical(self, "登录失败", "用户名或密码错误！")
            # messageBox("登录失败", "用户名或密码错误！",self)
    
    def customLogin(self):
        """跳转到客户登录页面"""
        config = getConfig()
        config["USER"]["USERNAME"] = ""
        config["USER"]["EMAIL"] = ""
        config["USER"]["PASSWORD"] = ""
        setConfig(config)
        # 登录后注册页面，动态加载内容
        # self.parent_window.register_page("todoList", TodoListPage(self.parent_window))
        # self.parent_window.register_page("settings", SettingsPage(self.parent_window))

        # 登陆界面不沉底
        # self.parent_window.unset_desktop_window()
        self.parent_window.switch_to_page("todoList", "right")
        self.parent_window.show_desktop()
        self.parent_window.set_desktop_window()
    
    def go_to_register(self):
        """跳转到注册页面"""
        # print("跳转到注册页面")
        self.parent_window.switch_to_page("register", "left")
        
    def fresh(self):
        return super().fresh()