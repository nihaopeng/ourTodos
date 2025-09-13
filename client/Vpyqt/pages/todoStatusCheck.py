from enum import IntEnum
import uuid
from pages.page import run_in_thread
from core.todo import TodoManager, TodoStep
from uipy.todoStatusCheckForm import Ui_Form as todoStatusCheckFormUI
from uipy.loadingForm import Ui_Form as LoadingFromUI
from PySide6.QtWidgets import QDialog,QWidget,QCheckBox,QHBoxLayout,QPushButton,QMessageBox
from core.todo import Todo

class TodoDialogResult(IntEnum):
    FINISHED = 1
    DELETED = 2
    UPLOADED = 3
    CLOSED = 4

class TodoStepCheckBox(QCheckBox):
    def __init__(self,todo:Todo,todoStep:TodoStep,todoManager:TodoManager,parent=None):
        super().__init__(todoStep.stepName,parent)
        self.todo = todo
        self.todoStep = todoStep
        self.toggled.connect(self.stepChecked)
        self.todoMamager = todoManager

    def stepChecked(self,checked):
        # print(checked,getTodoStep(self.todoUid))
        if checked:
            self.todoMamager.setTodoStep(self.todo.todoUid,self.todoStep.stepUid,"False")
        else:
            self.todoMamager.setTodoStep(self.todo.todoUid,self.todoStep.stepUid,"True")

class TodoStepWidget(QWidget):
    def __init__(self,todoStepCheckBox:TodoStepCheckBox,todoManager:TodoManager,parent):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # 去掉边距
        self.parent = parent

        self.todoStepCheckBox = todoStepCheckBox
        self.todoManager = todoManager
        self.delete_btn = QPushButton("❌", self)
        self.delete_btn.setFixedSize(24, 24)

        layout.addWidget(self.todoStepCheckBox)
        layout.addWidget(self.delete_btn)

        # 点击删除按钮时，删除自己
        self.delete_btn.clicked.connect(self.delete_self)
    
    def onSucDel(self,result):
        parent_layout = self.parentWidget().layout()
        if parent_layout:
            parent_layout.removeWidget(self)
        self.deleteLater()
        self.parent.loadingUi.hide()
    
    def delete_self(self):
        # 从数据库中删除
        self.parent.loadingUi.show()
        @run_in_thread(on_success=self.onSucDel,on_error=lambda e:(self.parent.loadingUi.hide(),QMessageBox.information(self,"错误",e)))
        def task():
            return self.todoManager.delTodoStep(self.todoStepCheckBox.todo.todoUid,self.todoStepCheckBox.todoStep.stepUid)
        task()
        # 从父布局移除并销毁自己
        

class TodoStatusCheckWindow(QDialog):
    """封装好的 Todo 状态检查窗口"""
    def __init__(self, todo:Todo,todoManager:TodoManager, parent=None):
        super().__init__(parent)
        self.ui = todoStatusCheckFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFromUI(self)

        self.todo = todo
        self.todoManager = todoManager

        # 初始化ui
        self.init()

        # 这里你可以额外绑定按钮功能
        self.ui.todoFinishedBtn.clicked.connect(self.on_finish)
        self.ui.todoDeleteBtn.clicked.connect(self.on_delete)
        self.ui.fileUploadBtn.clicked.connect(self.on_upload)
        self.ui.stepAddBtn.clicked.connect(self.stepAdd)
        # print(self.status)
        self.ui.todoFinishedBtn.setEnabled(True if self.todo.status=="True" else False)
        self.ui.fileUploadBtn.setEnabled(True if self.todo.status=="True" else False)

    def on_finish(self):
        # print(f"任务已完成: {self.ui.todoNameLabel.text()}")
        self.done(TodoDialogResult.FINISHED)

    def on_delete(self):
        # print(f"任务删除: {self.ui.todoNameLabel.text()}")
        self.done(TodoDialogResult.DELETED)   # 关闭窗口并返回 QDialog.Rejected

    def on_upload(self):
        # print("点击了上传按钮")
        pass

    def onSucStepAdd(self,result):
        # print("step add result:",result)
        self.loadingUi.hide()
        stepUid,stepContent = result
        todoStep = TodoStep(stepUid,stepContent,"True")
        todoStepCheckBox = TodoStepCheckBox(self.todo,todoStep,self.todoManager,self)
        todoStepWidget = TodoStepWidget(todoStepCheckBox,self.todoManager,self)
        self.ui.verticalLayout.insertWidget(self.ui.verticalLayout.count()-1,todoStepWidget)
        self.ui.stepLineEdit.clear()
    
    def stepAdd(self):
        stepContent = self.ui.stepLineEdit.text()
        if stepContent:
            self.loadingUi.show()
            @run_in_thread(on_success=self.onSucStepAdd,on_error=lambda e:(self.loadingUi.hide(),QMessageBox.information(self,"错误",e)))
            def task():
                # print("adding step,thread start:",stepContent)
                return self.todoManager.todoAddStep(self.todo.todoUid,0,stepContent)
            task()
            # return self.todoManager.todoAddStep(self.todo.todoUid,0,stepContent)
        else:
            QMessageBox.information(self,"错误","步骤内容不能为空")

    def closeEvent(self, event):
        event.accept()
        self.done(TodoDialogResult.CLOSED)

    def onSucInit(self,result):
        for item in result:
            stepUid = item[1]
            stepName = item[2]
            status = item[3]
            todoStep = TodoStep(stepUid,stepName,status)
            todoStepCheckBox = TodoStepCheckBox(self.todo,todoStep,self.todoManager,self)
            todoStepCheckBox.setChecked(True if status=="False" else False)
            todoStepWidget = TodoStepWidget(todoStepCheckBox,self.todoManager,self)
            self.ui.verticalLayout.insertWidget(self.ui.verticalLayout.count()-1,todoStepWidget)
        self.loadingUi.hide()

    def init(self):
        # 设置标题、名称、描述
        self.ui.todoNameLabel.setText(f"{self.todo.todoName} - 分数: {self.todo.score}")
        # self.ui.todoNameLabel.setText(self.name)
        self.ui.descriptionTextBrowser.setText(f"ddl:{self.todo.date}\n{self.todo.description}")

        # 从数据库初始化
        self.loadingUi.show()
        @run_in_thread(on_success=self.onSucInit,on_error=lambda e:(self.loadingUi.hide(),QMessageBox.information(self,"错误",e)))
        def task():
            return self.todoManager.getTodoStep(self.todo.todoUid)
        task()
        