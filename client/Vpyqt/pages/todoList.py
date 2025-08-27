
from PySide6.QtWidgets import (
    QWidget,QMessageBox,QPushButton,QCheckBox,QHBoxLayout
)
from core.config import getConfig
from pages.todoStatusCheck import TodoDialogResult, TodoStatusCheckWindow
from uipy.todoListForm import Ui_Form as TodoListFormUI
from core.todo import Todo, TodoManager
from PySide6.QtCore import QDate,QDateTime,QTimer
from uipy.loadingForm import Ui_Form as LoadingFromUI
from pages.rank import RankPage
from core.todo import Todo

class TodoButton(QPushButton):
    """待办事项按钮"""
    def __init__(self, todo:Todo,todoManager:TodoManager,parent=None):
        super().__init__(todo.todoName, parent)
        self.todo = todo
        self.todoMamager = todoManager
        self.setStyleSheet("padding: 5px; font-size: 16px;")
        self.setText(f"{todo.todoName} -{todo.date} {"" if todo.status == "True" else "√"}")
        self.setup_date_trigger()

    def setup_date_trigger(self):
        """根据到达日期设置定时触发器"""
        # print(self.date)
        target_dt = QDateTime.fromString(self.todo.date, "yyyy-MM-dd")
        now = QDateTime.currentDateTime()
        # print(target_dt,now)
        days_until_trigger = now.daysTo(target_dt)
        # print(days_until_trigger)
        
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
        self.setStyleSheet("padding: 10px; font-size: 16px;color:red;")

class TodoListPage(QWidget):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        self.todoManager = TodoManager()

        # 设置UI
        self.ui = TodoListFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFromUI(self)
        today = QDate.currentDate()
        self.ui.dateEdit.setDate(today)
        self.ui.dateEdit.setMinimumDate(today)

        # 连接信号与槽
        self.ui.settingsBtn.clicked.connect(self.gotoSettings)
        self.ui.addTodoBtn.clicked.connect(self.addTodo)
        self.ui.CoachBtn.clicked.connect(lambda: self.parent_window.switch_to_page("coach", "right"))
        self.ui.counterBtn.clicked.connect(lambda: self.parent_window.switch_to_page("counter","right"))
        self.ui.rankBtn.clicked.connect(self.gotoRank)

        # 加载todos
        self.loadTodos()

        # 初始化分数
        self.showScore()

    def loadTodos(self):
        """重新加载"""
        todos = self.todoManager.getTodos()
        for todo in todos:
            if todo.todoName and todo.description:
                self.addTodoItem(todo)

    def addTodo(self):
        """添加待办事项"""
        todoName = self.ui.todoLineEdit.text()
        todoDescription = self.ui.todoDescribeTextEdit.toPlainText()
        date = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        if not todoName and not todoDescription and not date:
            QMessageBox.warning(self, "输入错误", "待办事项和描述不能为空！")
            return
        # === 用线程异步生成分数 ===
        self.todoManager.addTodo(todoName,todoDescription,date)
        self.todoManager.scoreSignal.connect(lambda v:(self.addTodoItem(v),self.loadingUi.hide()))
        self.todoManager.errorSignal.connect(lambda v:(self.loadingUi.hide(),QMessageBox.information(self,"错误",v)))
        self.loadingUi.show()

    def addTodoItem(self,todo:Todo):
        """添加待办事项组件"""
        newTodo = TodoButton(todo,self.todoManager,self)
        newTodo.clicked.connect(lambda: self.toggleTodo(newTodo))
        self.ui.verticalLayout.insertWidget(0,newTodo)

    def toggleTodo(self,btn: TodoButton):
        # 用按钮本身的 name/description，而不是重新从输入框读
        dialog = TodoStatusCheckWindow(btn.todo,self.todoManager, self)
        result = dialog.exec()   # 模态显示

        if result == TodoDialogResult.FINISHED:
            self.todoManager.finishTodo(btn.todo.todoUid)
            btn.setText(f"{btn.todo.todoName} -{btn.todo.date} {"√"}")
            btn.todo.status = "False"
            self.ui.todoLineEdit.clear()
            self.ui.todoDescribeTextEdit.clear()
            self.showScore()
        elif result == TodoDialogResult.DELETED:
            self.delTodo(btn)

    def delTodo(self, btn: TodoButton):
        """删除待办事项"""
        # print("用户删除任务:", btn.todo.todoName)
        self.ui.verticalLayout.removeWidget(btn)  # 从布局移除
        btn.deleteLater()                         # 真正销毁
        # 从数据库销毁
        self.todoManager.delTodo(btn.todo.todoUid)
    
    def gotoSettings(self):
        """跳转到注册页面"""
        self.parent_window.switch_to_page("settings", "right")

    def showScore(self):
        config = getConfig()
        self.ui.scoreLabel.setText("score:"+config["USER"]["SCORE"])
    
    def gotoRank(self):
        self.parent_window.register_page("rank", RankPage(self.parent_window))
        self.parent_window.switch_to_page("rank", "right")