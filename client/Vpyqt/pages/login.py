
from PySide6.QtWidgets import (
    QWidget,QMessageBox
)
from pages.settings import SettingsPage
from pages.todoList import TodoListPage
from uipy.loginForm import Ui_Form as LoginFormUI

class LoginPage(QWidget):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        
        # 设置UI
        self.ui = LoginFormUI()
        self.ui.setupUi(self)

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
        if False:
            # 假设登录成功，跳转到待办事项页面
            from backend.config import getConfig, setConfig
            config = getConfig()
            config["USER"]["USERNAME"] = "admin"
            config["USER"]["PASSWORD"] = "admin123"
            config["USER"]["SCORE"] = "0" # 云端获取分数
            setConfig(config)
            self.parent_window.register_page("todoList", TodoListPage(self.parent_window))
            # QMessageBox.critical(self, "登录", "")
            self.parent_window.set_desktop_window()
            self.parent_window.switch_to_page("todoList", "right")
        else:
            QMessageBox.critical(self, "登录失败", "用户名或密码错误！")
            # messageBox("登录失败", "用户名或密码错误！",self)
    
    def customLogin(self):
        """跳转到客户登录页面"""
        from backend.config import getConfig, setConfig
        config = getConfig()
        config["USER"]["USERNAME"] = "customer"
        setConfig(config)
        # 登录后注册页面，动态加载内容
        self.parent_window.register_page("todoList", TodoListPage(self.parent_window))
        self.parent_window.register_page("settings", SettingsPage(self.parent_window))

        # 登陆后界面不沉底
        # self.parent_window.unset_desktop_window()
        self.parent_window.switch_to_page("todoList", "right")
        self.parent_window.show_desktop()
        self.parent_window.set_desktop_window()
    
    def go_to_register(self):
        """跳转到注册页面"""
        # print("跳转到注册页面")
        self.parent_window.switch_to_page("register", "left")