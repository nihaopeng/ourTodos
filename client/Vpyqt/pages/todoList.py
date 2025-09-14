
from PySide6.QtWidgets import (
    QMessageBox,QPushButton
)
from PySide6.QtCore import Qt
from core.user import UserManager
from pages.todoStatusCheck import TodoDialogResult, TodoStatusCheckWindow
from uipy.todoListForm import Ui_Form as TodoListFormUI
from core.todo import Todo, TodoManager
from PySide6.QtCore import QDate,QDateTime,QTimer
from uipy.loadingForm import Ui_Form as LoadingFromUI
from core.todo import Todo
from pages.page import Page, run_in_thread

class TodoButton(QPushButton):
    """待办事项按钮"""
    def __init__(self, todo:Todo,todoManager:TodoManager,parent=None):
        super().__init__(todo.todoName, parent)
        self.todo = todo
        self.todoMamager = todoManager
        self.setStyleSheet("padding: 5px; font-size: 16px;")
        self.setText(f"{todo.todoName} -{todo.date} {"" if todo.status == "True" else "√"}")
        self.setup_date_trigger()
        # self.setToolTip(self.text())
        self.setText(self.fontMetrics().elidedText(
            self.text(), 
            Qt.ElideRight, 
            self.width() - 20  # 留出一些边距
        ))

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

class TodoListPage(Page):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        self.todoManager = TodoManager()
        self.userManager = UserManager()
        
        # 设置UI
        self.ui = TodoListFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFromUI(self)
        today = QDate.currentDate()
        self.ui.dateEdit.setDate(today)
        self.ui.dateEdit.setMinimumDate(today)
        self.ui.todoListScrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.todoListScrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 连接信号与槽
        self.ui.settingsBtn.clicked.connect(self.gotoSettings)
        self.ui.addTodoBtn.clicked.connect(self.addTodo)
        self.ui.CoachBtn.clicked.connect(lambda: self.parent_window.switch_to_page("coach", "right"))
        self.ui.counterBtn.clicked.connect(lambda: self.parent_window.switch_to_page("counter","right"))
        self.ui.rankBtn.clicked.connect(self.gotoRank)
        self.todoManager.scoreSignal.connect(lambda v:(self.loadingUi.hide(),self.addTodoItem(v)))
        self.todoManager.errorSignal.connect(lambda v:(self.loadingUi.hide(),QMessageBox.information(self,"错误",v)))
        self.parent.pages["todoStatusCheck"].closeSignal.connect(self.todoStatusClose)
        self.parent.pages["todoStatusCheck"].deleteSignal.connect(self.todoStatusDelete)
        self.parent.pages["todoStatusCheck"].finishSignal.connect(self.todoStatusFinish)

    def clear_layout(self):
        # 减一避免删除掉布局的控件widget
        for i in reversed(range(self.ui.verticalLayout.count()-1)):
            item = self.ui.verticalLayout.itemAt(i)
            if item is None:
                continue
            # self.ui.verticalLayout.removeItem(item)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()

    def onSucLoadTodos(self,result):
        self.clear_layout()
        sorted(result,key=lambda x:(x.status,x.date))  # 先按状态再按日期排序
        for todo in result:
            if todo.todoName and todo.description:
                self.addTodoItem(todo)
        # self.showScore()
        self.loadingUi.hide()

    def loadTodos(self):
        """重新加载"""
        @run_in_thread(on_success=self.onSucLoadTodos,on_error=lambda e:(self.loadingUi.hide(),QMessageBox.information(self,"错误",e)))
        def task():
            return self.todoManager.getTodos()
        task()
        self.loadingUi.show()
    
    def addTodoItem(self,todo:Todo):
        """添加待办事项组件"""
        # print('add todo item:',todo.todoName)
        # print(todo)
        newTodo = TodoButton(todo,self.todoManager,self)
        # print("new todo:",newTodo.todo.todoName)
        newTodo.clicked.connect(lambda: self.toggleTodo(newTodo))
        self.ui.verticalLayout.insertWidget(0,newTodo)
        self.ui.todoLineEdit.clear()
        self.ui.todoDescribeTextEdit.clear()
        self.loadingUi.hide()

    def addTodo(self):
        """添加待办事项"""
        todoName = self.ui.todoLineEdit.text()
        todoDescription = self.ui.todoDescribeTextEdit.toPlainText()
        date = self.ui.dateEdit.date().toString("yyyy-MM-dd")
        if not todoName and not todoDescription and not date:
            QMessageBox.warning(self, "输入错误", "待办事项和描述不能为空！")
            return
        # === 用线程异步生成分数 ===
        self.loadingUi.show()
        @run_in_thread(on_success=self.addTodoItem,on_error=lambda e:(self.loadingUi.hide(),QMessageBox.information(self,"错误",e)))
        def task(todoName,todoDescription,date):
            return self.todoManager.addTodo(todoName,todoDescription,date)
        task(todoName,todoDescription,date)
        # self.todoManager.addTodo(todoName,todoDescription,date)
        
    def todoStatusClose(self):
        self.parent.switch_to_page("todoList","left")
        
    def todoStatusDelete(self,btn: TodoButton):
        self.delTodo(btn)
        self.parent.switch_to_page("todoList","left")
        
    def todoStatusFinish(self,btn: TodoButton):
        self.todoManager.finishTodo(btn.todo.todoUid)
        btn.setText(f"{btn.todo.todoName} -{btn.todo.date} {"√"}")
        btn.todo.status = "False"
        self.ui.todoLineEdit.clear()
        self.ui.todoDescribeTextEdit.clear()
        self.showScore()
        self.parent.switch_to_page("todoList","left")

    def toggleTodo(self,btn: TodoButton):
        # 用按钮本身的 name/description，而不是重新从输入框读
        # dialog = TodoStatusCheckWindow(btn.todo,self.todoManager, self)
        # result = dialog.exec()   # 模态显示

        # if result == TodoDialogResult.FINISHED:
        #     self.todoManager.finishTodo(btn.todo.todoUid)
        #     btn.setText(f"{btn.todo.todoName} -{btn.todo.date} {"√"}")
        #     btn.todo.status = "False"
        #     self.ui.todoLineEdit.clear()
        #     self.ui.todoDescribeTextEdit.clear()
        #     self.showScore()
        # elif result == TodoDialogResult.DELETED:
        #     self.delTodo(btn)
        self.parent.pages["todoStatusCheck"].todo = btn.todo
        self.parent.pages["todoStatusCheck"].todoBtn = btn
        self.parent.pages["todoStatusCheck"].todoManager = self.todoManager
        self.parent.switch_to_page("todoStatusCheck","right")

    def onSucDelTodo(self,result):
        self.loadingUi.hide()

    def delTodo(self, btn: TodoButton):
        """删除待办事项"""
        # print("用户删除任务:", btn.todo.todoName)
        self.ui.verticalLayout.removeWidget(btn)  # 从布局移除
        btn.deleteLater()                         # 真正销毁
        # 从数据库销毁
        self.loadingUi.show()
        @run_in_thread(on_success=self.onSucDelTodo,on_error=lambda e:(self.loadingUi.hide(),QMessageBox.information(self,"错误",e)))
        def task(todoUid):
            return self.todoManager.delTodo(todoUid)
        task(btn.todo.todoUid)
    
    def gotoSettings(self):
        """跳转到注册页面"""
        self.parent_window.switch_to_page("settings", "right")

    def onSucShowScore(self,result):
        status,score_or_reason = result
        if status:
            self.ui.scoreLabel.setText("score:"+score_or_reason)
        else:
            QMessageBox.information(self,"错误",score_or_reason)

    def showScore(self):
        @run_in_thread(on_success=self.onSucShowScore,on_error=lambda e:QMessageBox.information(self,"错误",e))
        def task():
            return self.userManager.getScore()
        task()
    
    def gotoRank(self):
        # self.parent_window.register_page("rank", RankPage(self.parent_window))
        self.parent_window.switch_to_page("rank", "right")
        
    def fresh(self):
        """刷新页面"""
        self.loadTodos()
        self.showScore()
        return super().fresh()