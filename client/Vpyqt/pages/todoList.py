
import uuid
from PySide6.QtWidgets import (
    QWidget,QMessageBox
)
from functools import partial
from backend.LLMCaller import LLMCaller
from backend.config import addTodo, getConfig, removeTodo, setConfig
from backend.provider import deepseek
from uipy.todoListForm import Ui_Form as TodoListFormUI
from todoM import Todo, TodoDialogResult, TodoStatusCheckWindow
from PySide6.QtCore import QObject, Signal, Slot, QThread,QDate
from uipy.loadingForm import Ui_Form as LoadingFromUI
from pages.rank import RankPage

class GenScoreWorker(QObject):
    finished = Signal(int)   # 生成完毕，返回分数
    error = Signal(str)      # 出错时发送
    def __init__(self, description, parent=None):
        super().__init__(parent)
        self.description = description

    @Slot()
    def run(self):
        try:
            llmCaller = LLMCaller()
            llmCaller.register_model("deepseek", deepseek.handler_factory)
            TEMPLATE = """
            用户画像如下：
            {personalProfile}
            考虑用户画像，并满足以下需求。
            {genScorePrompt}
            以下是待办的内容:
            <todo>
            {todo}
            </todo>
            """
            # TODO:加上判空逻辑
            query = TEMPLATE.format(personalProfile=getConfig()["USER"]["PERSONALPROFILE"],genScorePrompt=getConfig()["LLM"]["genScorePrompt"],todo=self.description)
        
            fulltext = ""
            for chunk in llmCaller.stream(query):
                fulltext += chunk

            score = int(fulltext.strip())
            self.finished.emit(score)
        except Exception as e:
            self.error.emit(str(e))

class TodoListPage(QWidget):
    """登录页面"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        if self.parent_window is None:
            raise ValueError("LoginPage 必须有一个父窗口")
        
        # 设置UI
        self.ui = TodoListFormUI()
        self.ui.setupUi(self)
        self.loadingUi = LoadingFromUI(self)
        today = QDate.currentDate()
        self.ui.dateEdit.setDate(today)
        self.ui.dateEdit.setMinimumDate(today)

        # 连接信号与槽
        self.ui.settingsBtn.clicked.connect(self.go_to_settings)
        self.ui.addTodoBtn.clicked.connect(self.add_todo)
        self.ui.CoachBtn.clicked.connect(lambda: self.parent_window.switch_to_page("coach", "right"))
        self.ui.counterBtn.clicked.connect(lambda: self.parent_window.switch_to_page("counter","right"))
        self.ui.rankBtn.clicked.connect(self.go_to_rank)

        # 加载todos
        self.loadTodos()

        # 初始化分数
        self.initScore()

    def loadTodos(self):
        """重新加载"""
        config = getConfig()
        if config["USER"]["USERNAME"]=="customer":
            # 游客登录，加载本地数据
            todos = config.get("TODO", [])
            # print(f"todos : {todos}")
        else:
            # 云端登录，加载云端数据
            # Todo
            todos = []
        for todo in todos:
            todoid = todo.get("uid", "")
            todoName = todo.get("name", "")
            todoDescription = todo.get("description", "")
            score = todo.get("score", 0)
            date = todo.get("date","")
            if todoName and todoDescription:
                self.add_todo_item(todoid,todoName, todoDescription,score,date)

    def add_todo(self):
        """添加待办事项"""
        todoName = self.ui.todoLineEdit.text()
        todoDescription = self.ui.todoDescribeTextEdit.toPlainText()
        if not todoName and not todoDescription:
            QMessageBox.warning(self, "输入错误", "待办事项和描述不能为空！")
            return
        # === 用线程异步生成分数 ===
        self.thread = QThread()
        self.worker = GenScoreWorker(todoDescription)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_genScore_finished)
        self.worker.error.connect(self.on_genScore_error)

        # 自动清理
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

        # 临时禁用按钮避免重复点
        # self.setStyleSheet("background-color: rgba(0, 0, 0, 0);")
        self.loadingUi.show()
        # self.ui.addTodoBtn.setEnabled(False)

    def on_genScore_finished(self, score):
        todoid = str(uuid.uuid4())
        todoName = self.ui.todoLineEdit.text()  # 注意：如果想用旧值，需要保存
        todoDescription = self.ui.todoDescribeTextEdit.toPlainText()
        todoDdl = self.ui.dateEdit.date().toString("yyyy-MM-dd")

        if getConfig()["USER"]["USERNAME"] == "customer":
            addTodo(todoid, todoName, todoDescription, score, todoDdl)
        else:
            # TODO: 云端保存
            pass

        self.add_todo_item(todoid, todoName, todoDescription, score,todoDdl)
        # 清空输入框
        self.ui.todoDescribeTextEdit.clear()
        self.ui.todoLineEdit.clear()  # 清空输入框

        # 关闭加载
        # self.styleSheet = self.originStyleSheet
        self.loadingUi.hide()
        self.thread.quit()
        # self.ui.addTodoBtn.setEnabled(True)

    def on_genScore_error(self, msg):
        QMessageBox.critical(self, "分数生成失败", f"错误: {msg}")
        self.loadingUi.hide()
        self.thread.quit()
        # self.ui.addTodoBtn.setEnabled(True)

    def add_todo_item(self,uid,todoName, todoDescription, score, dateDdl):
        """添加待办事项组件"""
        newTodo = Todo(uid,todoName, todoDescription,score,dateDdl,self)
        newTodo.clicked.connect(partial(self.toggle_todo,newTodo))
        self.ui.verticalLayout.insertWidget(0,newTodo)

    def toggle_todo(self,btn: Todo):
        # 用按钮本身的 name/description，而不是重新从输入框读
        todoUid = btn.uid
        todoName = btn.name
        todoDescription = btn.description
        score = btn.score
        date = btn.date

        dialog = TodoStatusCheckWindow(todoUid,todoName, todoDescription, score, date, self)
        result = dialog.exec()   # 模态显示

        if result == TodoDialogResult.FINISHED:
            self.scoreAdd(btn)
            self.delTodo(btn)
        elif result == TodoDialogResult.DELETED:
            self.delTodo(btn)

    def delTodo(self, btn: Todo):
        """删除待办事项"""
        print("用户删除任务:", btn.name)
        self.ui.verticalLayout.removeWidget(btn)  # 从布局移除
        btn.deleteLater()                         # 真正销毁
        # 从数据库销毁
        removeTodo(btn.uid)

    def scoreAdd(self, btn: Todo):
        config = getConfig()
        config["USER"]["SCORE"] = str(int(config["USER"]["SCORE"]) + btn.score)
        setConfig(config)
        self.ui.scoreLabel.setText(f"score:{int(config["USER"]["SCORE"])}")
    
    def go_to_settings(self):
        """跳转到注册页面"""
        self.parent_window.switch_to_page("settings", "right")

    def initScore(self):
        config = getConfig()
        self.ui.scoreLabel.setText("score:"+config["USER"]["SCORE"])
    
    def go_to_rank(self):
        self.parent_window.register_page("rank", RankPage(self.parent_window))
        self.parent_window.switch_to_page("rank", "right")