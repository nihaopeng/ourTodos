
from PySide6.QtWidgets import (
    QWidget,QColorDialog,QMessageBox
)
from core.settings import SettingsManager
from uipy.settingsForm import Ui_Form as SettingsFormUI
from pages.page import Page

class SettingsPage(Page):
    """设置页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.ui = SettingsFormUI()
        self.ui.setupUi(self)

        self.settingsManager = SettingsManager()

        # # 设置内容
        # self.initSettings()

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
        if self.settingsManager.saveUserinfoSettings(username,password,profile):
            QMessageBox.information(self, "保存成功", "设置已保存！")
        else:
            QMessageBox.information(self, "保存失败", "未知错误")
    
    def saveRemoteSettings(self):
        remoteUrl = self.ui.remoteUrlLineEdit.text()
        if not remoteUrl:
            QMessageBox.warning(self, "输入错误", "所有字段都不能为空！")
            return
        self.settingsManager.saveRemoteSettings(remoteUrl)
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
        self.settingsManager.saveModelSettings(provider,url,model,api_key,genScorePrompt)
        QMessageBox.information(self, "保存成功", "模型设置已保存！")

    def setColor(self, compo:str):
        color = QColorDialog.getColor()
        if not color.isValid():
            QMessageBox.information(self, "错误", "无效颜色！")
            return
        self.settingsManager.saveTheme(compo,color.name())
        QMessageBox.information(self, "成功", "设置成功，将重新登录以生效设置,可以重启软件以清除缓存")
        self.logout()

    def initSettings(self):
        # 设置内容
        config = self.settingsManager.getSettings()
        self.ui.usernameLineEdit.setText(config.get("USER", {}).get("USERNAME", ""))
        self.ui.passwordLineEdit.setText(config.get("USER", {}).get("PASSWORD", ""))
        self.ui.profileTextEdit.setText(config.get("USER", {}).get("PERSONALPROFILE", ""))
        self.ui.remoteUrlLineEdit.setText(config.get("REMOTE", {}).get("URL", ""))
        self.ui.providerLineEdit.setText(config.get("LLM", {}).get("PROVIDER", ""))
        self.ui.urlLineEdit.setText(config.get("LLM", {}).get("URL", ""))
        self.ui.modelLineEdit.setText(config.get("LLM", {}).get("MODEL_NAME", ""))
        self.ui.apikeyLineEdit.setText(config.get("LLM", {}).get("API_KEY", ""))
        self.ui.genScorePromptTextEdit.setText(config.get("LLM", {}).get("genScorePrompt", ""))
    
    def fresh(self):
        self.initSettings()
        return super().fresh()
