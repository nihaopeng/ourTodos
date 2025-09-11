import uuid

import requests
from core.config import getConfig, setConfig,request
import uuid
from core.LLMCaller import LLMCaller
from core.provider import deepseek
from PySide6.QtCore import QObject, Signal, Slot, QThread,QDate

class TodoStep():
    def __init__(self,stepUid,stepName,status) -> None:
        self.stepUid = stepUid
        self.stepName = stepName
        self.status = status

class Todo():
    def __init__(self,todoUid,name,description,score,date,status,steps):
        self.todoUid = todoUid
        self.todoName = name or ""
        self.description = description or ""
        self.score = score or 0
        self.date = date or "2025-01-01"
        self.status = status or "False"
        self.steps = []
        for step in steps:
            self.steps.append(TodoStep(step[0],step[1],step[2]))
    # def 

class AddTodoWorker(QObject):
    finished = Signal(int,str,int,str,str)   # 添加完成信号
    error = Signal(str)   # 出错信号
    
    def __init__(self, name, description, date, parent=None):
        super().__init__(parent)
        self.todoName = name
        self.todoDescription = description
        self.ddl = date
    
    @Slot()
    def run(self):
        try:
            data = {
                "email": getConfig()["USER"]["EMAIL"],
                "todoName": self.todoName,
                "todoDescription": self.todoDescription,
                "ddl": self.ddl,
            }
            res = request("add_todo", json=data)
            
            if res.json()["code"] != 200:
                raise Exception(f"Failed to add todo: {res.json().get('msg', 'Unknown error')}")
            
            self.finished.emit(res.json()["todoUid"],self.todoName,res.json()["score"],self.todoDescription,self.ddl)
        except Exception as e:
            self.error.emit(str(e))

class GenScoreWorker(QObject):
    finished = Signal(str,int,str,str)   # 生成完毕，返回分数
    error = Signal(str)      # 出错时发送
    def __init__(self,name,description,ddl,parent=None):
        super().__init__(parent)
        self.todoName = name
        self.description = description
        self.ddl = ddl

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
            # print(query)
            fulltext = ""
            for chunk in llmCaller.stream(query):
                fulltext += chunk

            score = int(fulltext.strip())
            self.finished.emit(self.todoName,score,self.description,self.ddl)
        except Exception as e:
            # print(e)
            self.error.emit(str(e))

class RemoteTodoManager(QObject):
    RemoteScoreSignal = Signal(Todo)
    RemoteErrorSignal = Signal(str)
    def __init__(self):
        super().__init__()
        self.todos = []

    def getTodos(self):
        data = {
            "email": getConfig()["USER"]["EMAIL"]
        }
        res = request("get_todos", json=data)
        todos = res.json()["todos"]
        self.todos.clear()
        for todo in todos:
            todoUid = todo[0]
            todoName = todo[1]
            todoDescription = todo[2]
            score = todo[4]
            date = todo[3]
            status = todo[5]
            steps = []
            self.todos.append(Todo(todoUid, todoName, todoDescription, score, date, status, steps))
        return self.todos

    def addTodo(self, name, description, date):
        # 创建线程和工作对象
        self.thread = QThread()
        self.add_worker = AddTodoWorker(name, description, date)
        self.add_worker.moveToThread(self.thread)
        
        # 连接信号和槽
        self.thread.started.connect(self.add_worker.run)
        self.add_worker.finished.connect(self.on_genScore_finished)
        self.add_worker.error.connect(self.on_genScore_error)
        
        # 自动清理
        self.add_worker.finished.connect(self.thread.quit)
        self.add_worker.finished.connect(self.add_worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        
        # 启动线程
        self.thread.start()

    def delTodo(self, todoUid):
        data = {
            "email": getConfig()["USER"]["EMAIL"],
            "todo_id": todoUid
        }
        res = request("del_todo", json=data)
        
        if res.json()["code"] != 200:
            raise Exception(f"Failed to delete todo: {res.json().get('msg', 'Unknown error')}")
        
        # 删除成功后，重新获取所有待办事项
        return self.getTodos()

    def finishTodo(self, todoUid):
        data = {
            "email": getConfig()["USER"]["EMAIL"],
            "todo_id": todoUid
        }
        res = request("todo_complete", json=data)
        
        if res.json()["code"] != 200:
            raise Exception(f"Failed to finish todo: {res.json().get('msg', 'Unknown error')}")
        
        # 完成待办后，重新获取所有待办事项
        return self.getTodos()

    def setTodoStep(self, todoUid, stepUid, status):
        data = {
            "email": getConfig()["USER"]["EMAIL"],
            "stepUid": stepUid,
            "status": status
        }
        res = request("step_change", json=data)
        
        if res.json()["code"] != 200:
            raise Exception(f"Failed to set todo step: {res.json().get('msg', 'Unknown error')}")
        
        return True

    def delTodoStep(self, todoUid, stepUid):
        data = {
            "email": getConfig()["USER"]["EMAIL"],
            "stepUid": stepUid
        }
        res = request("step_del", json=data)
        
        if res.json()["code"] != 200:
            raise Exception(f"Failed to delete todo step: {res.json().get('msg', 'Unknown error')}")
        
        return True

    def getTodoStep(self, todoUid):
        data = {
            "email": getConfig()["USER"]["EMAIL"],
            "todo_id": todoUid
        }
        res = request("get_steps", json=data)
        
        if res.json()["code"] != 200:
            raise Exception(f"Failed to get todo steps: {res.json().get('msg', 'Unknown error')}")
        
        return res.json().get("steps", [])

    def todoAddStep(self, todoUid, stepUid, stepName):
        data = {
            "email": getConfig()["USER"]["EMAIL"],
            "todo_id": todoUid,
            "stepName": stepName
        }
        res = request("step_add", json=data)
        
        if res.json()["code"] != 200:
            raise Exception(f"Failed to add todo step: {res.json().get('msg', 'Unknown error')}")
        
        return res.json()["stepUid"]
    
    def on_genScore_finished(self,todoUid,todoName,score,todoDescription,todoDdl):
        # print("Remote todo added:", todoName, score)
        newTodo = Todo(todoUid,todoName,todoDescription,score,todoDdl,"True",[])
        self.RemoteScoreSignal.emit(newTodo)
        # 关闭加载
        self.thread.quit()
        # self.ui.addTodoBtn.setEnabled(True)

    def on_genScore_error(self, msg):
        # self.loadingUi.hide()
        self.RemoteErrorSignal.emit(msg)
        self.thread.quit()

class CustomerTodoManager(QObject):
    CustomerScoreSignal = Signal(Todo)
    CustomerErrorSignal = Signal(str)
    def __init__(self):
        super().__init__()
        self.todos = []

    def getTodos(self):
        config = getConfig()
        todos = config.get("TODO", [])
        # print(todos)
        self.todos.clear()
        for todo in todos:
            todoUid = todo.get("uid", "")
            todoName = todo.get("name", "")
            todoDescription = todo.get("description", "")
            score = todo.get("score", 0)
            date = todo.get("date","")
            status = todo.get("status","")
            steps = todo.get("steps",[])
            self.todos.append(Todo(todoUid,todoName,todoDescription,score,date,status,steps))
        return self.todos
    
    def addTodo(self,name,description,date):
        # === 用线程异步生成分数 ===
        self.thread = QThread()
        self.worker = GenScoreWorker(name,description,date)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_genScore_finished)
        self.worker.error.connect(self.on_genScore_error)
        # 自动清理
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()
    
    def delTodo(self,todoUid):
        data = getConfig()
        before = len(data.get("TODO", []))
        data["TODO"] = [c for c in data.get("TODO", []) if c["uid"] != todoUid]
        if len(data["TODO"]) == before:
            raise ValueError(f"{todoUid} 不存在")
        setConfig(data)

    def finishTodo(self,todoUid):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        data = getConfig()
        todo_list = data.get("TODO", [])
        # 查找对应 uid
        for item in todo_list:
            if item["uid"] == todoUid:
                # 确保 item 有 step 列表
                item["status"] = "False"
                data["USER"]["SCORE"] = str(int(data["USER"]["SCORE"]) + int(item["score"]))
                setConfig(data)  # 保存更新
                return  # 添加完成后返回
        raise ValueError(f"TODO uid={todoUid} 不存在")
            
    def setTodoStep(self,todoUid,stepUid,status):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        data = getConfig()
        todo_list = data.get("TODO", [])
        # 查找对应 uid
        for item in todo_list:
            if item["uid"] == todoUid:
                # 确保 item 有 step 列表
                # print(item["step"][stepIndex])
                for i,tmp in enumerate(item["step"]):
                    if tmp[0]==stepUid:
                        item["step"][i][2]=status
                        setConfig(data)
                        return
        # 如果没有找到对应 uid
        raise ValueError(f"TODO uid={todoUid} 不存在")
    
    def delTodoStep(self,todoUid,stepUid):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        data = getConfig()
        todo_list = data.get("TODO", [])
        # 查找对应 uid
        for item in todo_list:
            if item["uid"] == todoUid:
                # 确保 item 有 step 列表
                for tmp in item["step"]:
                    if tmp[0]==stepUid:
                        item["step"].remove(tmp)
                        setConfig(data)
                        return
        # 如果没有找到对应 uid
        raise ValueError(f"TODO uid={todoUid} 不存在")
    
    def getTodoStep(self,todoUid):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        data = getConfig()
        todo_list = data.get("TODO", [])
        # 查找对应 uid
        for item in todo_list:
            if item["uid"] == todoUid:
                # 确保 item 有 step 列表
                return item["step"] # 添加完成后返回
        # 如果没有找到对应 uid
        raise ValueError(f"TODO uid={todoUid} 不存在")
    
    def todoAddStep(self,todoUid,stepUid,stepName):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        data = getConfig()
        todo_list = data.get("TODO", [])
        
        # 查找对应 uid
        for item in todo_list:
            if item["uid"] == todoUid:
                # 确保 item 有 step 列表
                if "step" not in item or not isinstance(item["step"], list):
                    item["step"] = []
                item["step"].append([stepUid,stepName,"False"])
                setConfig(data)  # 保存更新
                return  # 添加完成后返回
        
        # 如果没有找到对应 uid
        raise ValueError(f"TODO uid={todoUid} 不存在")
    
    def on_genScore_finished(self,todoName,score,todoDescription,todoDdl):
        todoUid = str(uuid.uuid4())
        self.addTodo2config(todoUid, todoName, todoDescription, score, todoDdl)
        newTodo = Todo(todoUid,todoName,todoDescription,score,todoDdl,"True",[])
        self.CustomerScoreSignal.emit(newTodo)
        # 关闭加载
        self.thread.quit()
        # self.ui.addTodoBtn.setEnabled(True)

    def on_genScore_error(self, msg):
        # self.loadingUi.hide()
        self.CustomerErrorSignal.emit(msg)
        self.thread.quit()

    def addTodo2config(self,todoid, todoName, todoDescription, score, todoDdl):
        data = getConfig()
        # 避免重复
        for cat in data.get("TODO", []):
            if cat["uid"] == todoid:
                raise ValueError(f"{todoid} 已存在")
        data.setdefault("TODO", []).append({
            "uid":todoid,
            "name": todoName,
            "description": todoDescription,
            "score": score,
            "step":[],
            "date":todoDdl,
            "status":"True"
        })
        setConfig(data)

    def finishTodo(self,todoUid):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        data = getConfig()
        todo_list = data.get("TODO", [])
        # 查找对应 uid
        for item in todo_list:
            if item["uid"] == todoUid:
                # 确保 item 有 step 列表
                item["status"] = "False"
                data["USER"]["SCORE"] = str(int(item["score"])+int(data["USER"]["SCORE"]))
                setConfig(data)  # 保存更新
                return  # 添加完成后返回
        # 如果没有找到对应 uid
        raise ValueError(f"TODO uid={todoUid} 不存在")

class TodoManager(QObject):
    scoreSignal = Signal(Todo)
    errorSignal = Signal(str)
    def __init__(self) -> None:
        super().__init__()
        self.customerTodoManager = CustomerTodoManager()
        self.remoteTodoManager = RemoteTodoManager()
        self.customerTodoManager.CustomerScoreSignal.connect(lambda v:(self.scoreSignal.emit(v)))
        self.customerTodoManager.CustomerErrorSignal.connect(lambda v:(self.errorSignal.emit(v)))
        self.remoteTodoManager.RemoteScoreSignal.connect(lambda v:(self.scoreSignal.emit(v)))
        self.remoteTodoManager.RemoteErrorSignal.connect(lambda v:(self.errorSignal.emit(v)))

    def getTodos(self) -> list[Todo]:
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.getTodos()
        else:
            return self.remoteTodoManager.getTodos()
        
    def addTodo(self,name,description,date):
        # === 用线程异步生成分数 ===
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.addTodo(name,description,date)
        else:
            return self.remoteTodoManager.addTodo(name,description,date)
        
    def delTodo(self,todoUid):
        # === 用线程异步生成分数 ===
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.delTodo(todoUid)
        else:
            return self.remoteTodoManager.delTodo(todoUid)
        
    def finishTodo(self,todoUid):
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.finishTodo(todoUid)
        else:
            return self.remoteTodoManager.finishTodo(todoUid)
    
    def setTodoStep(self,todoUid,stepUid,status):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.setTodoStep(todoUid,stepUid,status)
        else:
            return self.remoteTodoManager.setTodoStep(todoUid,stepUid,status)
        
    def delTodoStep(self,todoUid,stepUid):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.delTodoStep(todoUid,stepUid)
        else:
            return self.remoteTodoManager.delTodoStep(todoUid,stepUid)
        
    def getTodoStep(self,todoUid):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.getTodoStep(todoUid)
        else:
            return self.remoteTodoManager.getTodoStep(todoUid)
        
    def todoAddStep(self,todoUid,stepUid,stepName):
        """
        给指定 uid 的 todo 项添加一个步骤字符串
        """
        config = getConfig()
        if config["USER"]["USERNAME"]=="":
            return self.customerTodoManager.todoAddStep(todoUid,stepUid,stepName)
        else:
            return self.remoteTodoManager.todoAddStep(todoUid,stepUid,stepName)