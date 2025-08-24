import uuid
from backend.config import delTodoStep, getTodoStep, setTodoStep, todoAddStep
from uipy.todoStatusCheckForm import Ui_Form as todoStatusCheckFormUI
from PySide6.QtWidgets import QDialog, QPushButton,QCheckBox,QWidget,QHBoxLayout,QMessageBox
from PySide6.QtCore import QTimer, QDateTime
from enum import IntEnum

class TodoDialogResult(IntEnum):
    FINISHED = 1
    DELETED = 2
    UPLOADED = 3
    CLOSED = 4

class TodoStatusCheckWindow(QDialog):
    """封装好的 Todo 状态检查窗口"""
    def __init__(self, uid:str,name: str, description: str,score: int,date:str, parent=None):
        super().__init__(parent)
        self.ui = todoStatusCheckFormUI()
        self.ui.setupUi(self)

        self.uid = uid
        self.name = name
        self.description = description
        self.score = score
        self.date=date

        # 初始化ui
        self.init()

        # 这里你可以额外绑定按钮功能
        self.ui.todoFinishedBtn.clicked.connect(self.on_finish)
        self.ui.todoDeleteBtn.clicked.connect(self.on_delete)
        self.ui.fileUploadBtn.clicked.connect(self.on_upload)
        self.ui.stepAddBtn.clicked.connect(self.stepAdd)

    def on_finish(self):
        # print(f"任务已完成: {self.ui.todoNameLabel.text()}")
        self.done(TodoDialogResult.FINISHED)

    def on_delete(self):
        # print(f"任务删除: {self.ui.todoNameLabel.text()}")
        self.done(TodoDialogResult.DELETED)   # 关闭窗口并返回 QDialog.Rejected

    def on_upload(self):
        # print("点击了上传按钮")
        pass
    
    def stepAdd(self):
        stepContent = self.ui.stepLineEdit.text()
        if stepContent:
            stepUid = str(uuid.uuid4())
            todoAddStep(self.uid,stepUid,stepContent)
            todoStep = TodoStep(self.uid,stepUid,stepContent,"False",self)
            todoStepWidget = TodoStepWidget(todoStep,self)
            self.ui.verticalLayout.insertWidget(self.ui.verticalLayout.count()-1,todoStepWidget)
            self.ui.stepLineEdit.clear()

    def closeEvent(self, event):
        event.accept()
        self.done(TodoDialogResult.CLOSED)

    def init(self):
        # 设置标题、名称、描述
        self.ui.todoNameLabel.setText(f"{self.name} - 分数: {self.score}")
        # self.ui.todoNameLabel.setText(self.name)
        self.ui.descriptionTextBrowser.setText(f"ddl:{self.date}\n{self.description}")

        # 从数据库初始化
        steps = getTodoStep(self.uid)
        # print(steps)
        for item in steps:
            stepid = item[0]
            step = item[1]
            stat = item[2]
            todoStep = TodoStep(self.uid,stepid,step,False,self)
            todoStep.setChecked(True if stat=="True" else False)
            todoStepWidget = TodoStepWidget(todoStep,self)
            self.ui.verticalLayout.insertWidget(self.ui.verticalLayout.count()-1,todoStepWidget)


class Todo(QPushButton):
    """待办事项按钮"""
    def __init__(self, uid,name, description,score,date,parent=None):
        super().__init__(name, parent)
        self.uid = uid
        self.name = name
        self.description = description
        self.score = score
        self.date = date
        self.setStyleSheet("padding: 5px; font-size: 16px;")
        self.setText(f"{name} -{self.date}")
        self.setup_date_trigger()
        # self.clicked.connect(self.toggle_todo)
    def setup_date_trigger(self):
        """根据到达日期设置定时触发器"""
        # print(self.date)
        target_dt = QDateTime.fromString(self.date, "yyyy-MM-dd")
        now = QDateTime.currentDateTime()
        # print(target_dt,now)
        days_until_trigger = now.daysTo(target_dt)
        print(days_until_trigger)
        
        if days_until_trigger > 0:
            timer = QTimer(self)
            timer.setSingleShot(True)
            timer.timeout.connect(self.on_date_reached)
            timer.start(days_until_trigger*24*60*60)  # 延迟触发
        else:
            # 如果时间已过，可立即触发或忽略
            self.on_date_reached()
    
    def on_date_reached(self):
        """到达日期时的动作"""
        # QMessageBox.information(self, "提醒", f"待办事项 '{self.name}' 到达日期！")
        # 你也可以修改按钮样式，或执行其他逻辑
        self.setStyleSheet("padding: 10px; font-size: 16px;color:red;")

class TodoStep(QCheckBox):
    def __init__(self,todoUid,stepid,step,stat,parent=None):
        super().__init__(step,parent)
        self.todoUid = todoUid
        self.stepid = stepid
        self.stat = stat
        self.step = step
        
        self.toggled.connect(self.stepChecked)

    def stepChecked(self,checked):
        # print(checked,getTodoStep(self.todoUid))
        if checked:
            setTodoStep(self.todoUid,self.stepid,"True")
        else:
            setTodoStep(self.todoUid,self.stepid,"False")

class TodoStepWidget(QWidget):
    def __init__(self,todoStep:TodoStep,parent):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 去掉边距

        self.todoStep = todoStep
        self.delete_btn = QPushButton("❌", self)
        self.delete_btn.setFixedSize(24, 24)

        layout.addWidget(self.todoStep)
        layout.addWidget(self.delete_btn)

        # 点击删除按钮时，删除自己
        self.delete_btn.clicked.connect(self.delete_self)
    
    def delete_self(self):
        # 从数据库中删除
        delTodoStep(self.todoStep.todoUid,self.todoStep.stepid)
        # 从父布局移除并销毁自己
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            parent_layout.removeWidget(self)
        self.deleteLater()

