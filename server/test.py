import requests

BASE = "http://127.0.0.1:5000"   # Flask 服务地址

# ========== 用户相关 ==========
def test_register():
    data = {
        "username": "alice",
        "email": "alice@test.com",
        "password": "123456"
    }
    r = requests.post(f"{BASE}/regist", json=data)
    print("注册:", r.json())

def test_login():
    data = {
        "email": "alice@test.com",
        "password": "123456"
    }
    r = requests.post(f"{BASE}/login", json=data)
    print("登录:", r.json())

# ========== Todo 相关 ==========
def test_add_todo():
    data = {
        "todoName": "写论文",
        "todoDescription": "完成方法章节",
        "ddl": "2025-09-01",
        "score": 10,
        "email": "alice@test.com"
    }
    r = requests.post(f"{BASE}/add_todo", json=data)
    print("添加待办:", r.json())

def test_del_todo(todo_id):
    data = {"todo_id": todo_id}
    r = requests.post(f"{BASE}/del_todo", json=data)
    print("删除待办:", r.json())

def test_todo_complete(todo_id):
    data = {"todo_id": todo_id, "email": "alice@test.com"}
    r = requests.post(f"{BASE}/todo_complete", json=data)
    print("完成待办:", r.json())

def test_step_change(todo_id):
    data = {
        "todo_id": todo_id,
        "steps": [
            {"stepName": "查文献", "status": "True"},
            {"stepName": "写代码", "status": "False"}
        ]
    }
    r = requests.post(f"{BASE}/step_change", json=data)
    print("步骤变更:", r)

# ========== 积分相关 ==========
def test_get_user_score():
    data = {"email": "alice@test.com"}
    r = requests.post(f"{BASE}/get_user_score", json=data)
    print("获取用户积分:", r.json())

def test_get_scores():
    r = requests.get(f"{BASE}/get_scores")
    print("所有用户积分:", r.json())

# ========== 测试执行 ==========
if __name__ == "__main__":
    # 1. 注册用户
    test_register()
    # 2. 登录
    test_login()
    # 3. 添加待办
    test_add_todo()

    # 假设添加的待办 id = 1（你可以在数据库查实际 todoid）
    todo_id = 1

    # 4. 修改步骤
    test_step_change(todo_id)
    # 5. 完成任务
    test_todo_complete(todo_id)
    # 6. 查询积分
    test_get_user_score()
    test_get_scores()
    # 7. 删除任务
    test_del_todo(todo_id)
