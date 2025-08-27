import requests

BASE = "http://127.0.0.1:5000"   # Flask 服务地址

req = requests.Session()

# ========== 用户相关 ==========
def test_register(username,email,password):
    data = {
        "username": username,
        "email": email,
        "password": password
    }
    r = req.post(f"{BASE}/regist", json=data)
    print("注册:", r.json())

def test_login(email,password):
    data = {
        "email": email,
        "password": password
    }
    r = req.post(f"{BASE}/login", json=data)
    print("登录:", r.json())

# ========== Todo 相关 ==========
def test_get_todos(email):
    data = {"email":email}
    r = req.post(f"{BASE}/get_todos", json=data)
    print("获取待办:", r.json()["todos"])
    return r.json()["todos"]

def test_add_todo(todoName,todoDescription,ddl,score,email):
    data = {
        "todoName": todoName,
        "todoDescription": todoDescription,
        "ddl": ddl,
        "score": score,
        "email": email
    }
    r = req.post(f"{BASE}/add_todo", json=data)
    print("添加待办:", r.json())
    if r.json()["code"]==200:
        return r.json()["todoUid"]
    else:
        return None

def test_del_todo(email,todo_id):
    data = {"todo_id": todo_id,"email":email}
    r = req.post(f"{BASE}/del_todo", json=data)
    print("删除待办:", r.json())

def test_todo_complete(todo_id,email):
    data = {"todo_id": todo_id, "email": email}
    r = req.post(f"{BASE}/todo_complete", json=data)
    print("完成待办:", r.json())

def test_get_steps(todoUid,email):
    data = {
        "todo_id": todoUid,
        "email":email
    }
    r = req.post(f"{BASE}/get_steps", json=data)
    print("步骤获取:", r.json())

def test_step_add(todo_id,stepName,email):
    data = {
        "todo_id": todo_id,
        "stepName": stepName,
        "email":email
    }
    r = req.post(f"{BASE}/step_add", json=data)
    print("新增步骤:", r.json())
    if r.json()["code"]==200:
        return r.json()["stepUid"]
    else:
        return None

def test_step_del(stepUid,email):
    data = {
        "stepUid": stepUid,
        "email":email
    }
    r = req.post(f"{BASE}/step_del", json=data)
    print("步骤删除:", r)

def test_step_change(stepUid,status,email):
    data = {
        "stepUid": stepUid,
        "status":status,
        "email":email
    }
    r = req.post(f"{BASE}/step_change", json=data)
    print("步骤变更:", r)

# ========== 积分相关 ==========
def test_get_user_score(email):
    data = {"email": email}
    r = req.post(f"{BASE}/get_user_score", json=data)
    print("获取用户积分:", r.json())

def test_get_scores(email):
    data = {"email": email}
    r = req.get(f"{BASE}/get_scores",json=data)
    print("所有用户积分:", r.json())

# ========== 测试执行 ==========
if __name__ == "__main__":
    # 1. 注册用户
    test_register("1","1@qq.com","123")
    test_register("2","2@qq.com","123")
    test_register("3","3@qq.com","123")
    # 2. 登录
    test_login("2@qq.com","123")
    # 3. 添加待办
    todo1id = test_add_todo("test","this is a test","2025-08-27","123","2@qq.com")
    todo2id = test_add_todo("test1","this is a test1","2025-08-28","12","2@qq.com")
    todo3id = test_add_todo("test","this is a test","2025-08-27","123","1@qq.com")# 未登录

    # 查看待办
    test_get_todos("2@qq.com")
    # 4. 增加步骤
    step1id = test_step_add(todo1id,"step1","2@qq.com")
    step2id = test_step_add(todo1id,"step2","2@qq.com")
    step3id = test_step_add(todo1id,"step3","2@qq.com")
    step4id = test_step_add(todo1id,"step1","1@qq.com")# 错误邮箱
    # 查看步骤
    test_get_steps(todo1id,"2@qq.com")
    # 5. 删除步骤
    test_step_del(step1id,"2@qq.com")
    # 6, 完成步骤
    test_step_change(step2id,"False","2@qq.com")
    # 完成待办
    test_todo_complete(todo1id,"2@qq.com")
    # 6. 查询积分
    test_get_user_score("2@qq.com")
    test_get_scores("2@qq.com")
    # 7. 删除任务
    test_del_todo("2@qq.com",todo2id)
