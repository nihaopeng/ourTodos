from PySide6.QtWidgets import (
    QWidget, 
    QMessageBox
)
from uipy.registerForm import Ui_Form as RegisterFormUI

class RegisterPage(QWidget):
    """注册页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        
        # 设置UI
        self.ui = RegisterFormUI()
        self.ui.setupUi(self)
        
        # 连接信号
        self.ui.registerBtn.clicked.connect(self.attempt_register)
        self.ui.back2loginBtn.clicked.connect(self.go_to_login)
        # self.ui..clicked.connect(self.go_to_login)
    
    def attempt_register(self):
        """尝试注册"""
        username = self.ui.usernameLineEdit.text()
        email = self.ui.emailLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        
        if not username or not email or not password:
            QMessageBox.warning(self, "输入错误", "所有字段都必须填写！")
            return
            
        # 在实际应用中，这里会有注册逻辑
        QMessageBox.information(self, "注册成功", f"用户 {username} 注册成功！")
        self.go_to_login()
    
    def go_to_login(self):
        """跳转到登录页面"""
        self.parent_window.switch_to_page("login", "right")