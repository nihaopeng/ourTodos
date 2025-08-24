
import sys
from PySide6.QtWidgets import (
    QWidget,QColorDialog,QMessageBox
)
from PySide6.QtCore import QTimer
from uipy.settingsForm import Ui_Form as SettingsFormUI
from backend.config import setConfig, getConfig

class SettingsPage(QWidget):
    """设置页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.ui = SettingsFormUI()
        self.ui.setupUi(self)

        # 设置内容
        self.initSettings()

        # 连接信号与槽
        self.ui.back2homeBtn.clicked.connect(self.go_to_home)
        self.ui.saveUserInfoBtn.clicked.connect(self.saveUserinfoSettings)
        self.ui.saveRemoteBtn.clicked.connect(self.saveRemoteSettings)
        self.ui.saveModelBtn.clicked.connect(self.saveModelSettings)
        self.ui.buttonColorBtn.clicked.connect(lambda: self.setColor("btn"))
        self.ui.buttonHoverColorBtn.clicked.connect(lambda: self.setColor("btnHover"))
        self.ui.backgroundColorBtn.clicked.connect(lambda: self.setColor("bg"))
        self.ui.fontColorBtn.clicked.connect(lambda: self.setColor("font"))
        self.ui.logoutBtn.clicked.connect(self.logout)

    def logout(self):
        self.parent_window.unset_desktop_window()
        self.parent_window.switch_to_page("login", "left")

    def go_to_home(self):
        """跳转到主页"""
        self.parent_window.switch_to_page("todoList", "left")

    def saveUserinfoSettings(self):
        """保存用户设置"""
        username = self.ui.usernameLineEdit.text()
        password = self.ui.passwordLineEdit.text()
        profile = self.ui.profileTextEdit.toPlainText()

        if not username or not password:
            QMessageBox.warning(self, "输入错误", "所有字段都不能为空！")
            return

        # 这里可以添加保存逻辑，比如保存到配置文件或数据库
        config = getConfig()
        config["USER"]["PERSONALPROFILE"] = profile
        setConfig(config)
        # TODO:保存用户信息到远端
        QMessageBox.information(self, "保存成功", "设置已保存！")
    
    def saveRemoteSettings(self):
        remoteUrl = self.ui.remoteUrlLineEdit.text()
        if not remoteUrl:
            QMessageBox.warning(self, "输入错误", "所有字段都不能为空！")
            return
        
        config = getConfig()
        config["REMOTE"]["URL"] = remoteUrl
        setConfig(config)
        QMessageBox.information(self, "保存成功", "设置已保存！")

    def saveModelSettings(self):
        """保存模型设置"""
        provider = self.ui.providerLineEdit.text()
        url = self.ui.urlLineEdit.text()
        model = self.ui.modelLineEdit.text()
        api_key = self.ui.apikeyLineEdit.text()
        genScorePrompt = self.ui.genScorePromptTextEdit.toPlainText()
        if not provider or not url or not model or not api_key or not genScorePrompt:
            QMessageBox.warning(self, "输入错误", "所有字段都不能为空！")
            return
        # 这里可以添加保存逻辑，比如保存到配置文件或数据库
        config = getConfig()
        config["LLM"]["PROVIDER"] = provider
        config["LLM"]["URL"] = url
        config["LLM"]["MODEL_NAME"] = model
        config["LLM"]["API_KEY"] = api_key
        config["LLM"]["genScorePrompt"] = genScorePrompt
        setConfig(config)
        QMessageBox.information(self, "保存成功", "模型设置已保存！")

    def setColor(self, compo:str):
        color = QColorDialog.getColor()
        config = getConfig()
        if not color.isValid():
            QMessageBox.information(self, "错误", "无效颜色！")
            return
        if compo == "btn":
            config["THEME"]["BTNCOLOR"] = color.name()
        elif compo == "btnHover":
            config["THEME"]["BTNHOVERCOLOR"] = color.name()
        elif compo == "bg":
            config["THEME"]["BGCOLOR"] = color.name()
        elif compo == "font":
            config["THEME"]["FONTCOLOR"] = color.name()
        else:
            QMessageBox.information(self, "错误", "未知错误")
        setConfig(config)
        QMessageBox.information(self, "成功", "设置成功，将重新登录以生效设置")
        self.logout()

    def initSettings(self):
        # 设置内容
        config = getConfig()
        self.ui.usernameLineEdit.setText(config.get("USER", {}).get("USERNAME", ""))
        self.ui.passwordLineEdit.setText(config.get("USER", {}).get("PASSWORD", ""))
        self.ui.remoteUrlLineEdit.setText(config.get("REMOTE", {}).get("URL", ""))
        self.ui.providerLineEdit.setText(config.get("LLM", {}).get("PROVIDER", ""))
        self.ui.urlLineEdit.setText(config.get("LLM", {}).get("URL", ""))
        self.ui.modelLineEdit.setText(config.get("LLM", {}).get("MODEL_NAME", ""))
        self.ui.apikeyLineEdit.setText(config.get("LLM", {}).get("API_KEY", ""))
        self.ui.genScorePromptTextEdit.setText(config.get("LLM", {}).get("genScorePrompt", ""))
