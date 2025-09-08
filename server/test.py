import requests

BASE = "http://127.0.0.1:5000"   # Flask 服务地址

req = requests.Session()

# ========== 用户相关 ==========
def test_send_code(email):
    data = {
        "email": email
    }
    r = req.post(f"{BASE}/send_verification_code", json=data)
    print("验证:", r.json())

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

def test_update_username_and_password(email,newUsername,newPassword):
    data = {
        "email":email,
        "username":newUsername,
        "password":newPassword
    }
    r = req.post(f"{BASE}/update_username_and_password", json=data)
    print("修改:", r.json())


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
    print("步骤删除:", r.json())

def test_step_change(stepUid,status,email):
    data = {
        "stepUid": stepUid,
        "status":status,
        "email":email
    }
    r = req.post(f"{BASE}/step_change", json=data)
    print("步骤变更:", r.json())

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
    # 1. 测试用户系统
    test_send_code("YutaoPeng@foxmail.com")
    # test_register("1","1@qq.com","123")
    # test_register("2","2@qq.com","123")
    # test_login("1@qq.com","124")
    # test_login("2@qq.com","123")
    # test_update_username_and_password("2@qq.com","new_2","new_123")
    # test_login("2@qq.com","new_123")
    # # 测试todo系统
    # test_add_todo("todo1","none","2025-07-01","12","1@qq.com")
    # todo1 = test_add_todo("todo1","读一本书","2025-07-01","12","2@qq.com")
    # todo2 = test_add_todo("todo2","写一篇论文","2025-07-01","11","2@qq.com")
    # todo3 = test_add_todo("todo3","实现一个函数","2025-07-01","10","2@qq.com")
    # step1Uid_todo1 = test_step_add(todo1,"step1Uid_todo1","2@qq.com")
    # step2Uid_todo1 = test_step_add(todo1,"step2Uid_todo1","2@qq.com")
    # step3Uid_todo1 = test_step_add(todo1,"step3Uid_todo1","2@qq.com")
    # test_get_steps(todo1,"2@qq.com")
    # step1Uid_todo2 = test_step_add(todo2,"step1Uid_todo2","2@qq.com")
    # test_get_steps(todo1,"2@qq.com")
    # step2Uid_todo2 = test_step_add(todo2,"step2Uid_todo2","2@qq.com")
    # step1Uid_todo3 = test_step_add(todo2,"step1Uid_todo3","2@qq.com")
    # step2Uid_todo3 = test_step_add(todo2,"step2Uid_todo3","2@qq.com")
    # test_get_steps(todo2,"2@qq.com")
    # test_step_change(step1Uid_todo1,"False","2@qq.com")
    # test_step_del(step2Uid_todo1,"2@qq.com")
    # test_del_todo("2@qq.com",todo2)
    # test_get_scores("2@qq.com")
    # test_get_user_score("1@qq.com")
    # test_todo_complete(todo3,"2@qq.com")
    # test_get_user_score("1@qq.com")
    # test_get_scores("2@qq.com")



    


    
