import requests
import toml
import os

config_path = os.path.join(os.path.dirname(__file__),"config.toml")

req = requests.session()

def getConfig():
    return toml.load(config_path)

def setConfig(config):
    with open(config_path, "w",encoding='utf-8') as f:
        toml.dump(config, f)
    return

def request(route:str,json:dict):
    return req.post(f"{getConfig()["REMOTE"]["URL"]}/{route}",json=json)

# def finishTodo(uid):
#     """
#     给指定 uid 的 todo 项添加一个步骤字符串
#     """
#     data = getConfig()
#     todo_list = data.get("TODO", [])
    
#     # 查找对应 uid
#     for item in todo_list:
#         if item["uid"] == uid:
#             # 确保 item 有 step 列表
#             item["status"] = "False"
#             setConfig(data)  # 保存更新
#             return  # 添加完成后返回
    
#     # 如果没有找到对应 uid
#     raise ValueError(f"TODO uid={uid} 不存在")

# def addTodo(uid,name, description, score, date):
#     data = getConfig()
#     # 避免重复
#     for cat in data.get("TODO", []):
#         if cat["uid"] == uid:
#             raise ValueError(f"{uid} 已存在")
#     data.setdefault("TODO", []).append({
#         "uid":uid,
#         "name": name,
#         "description": description,
#         "score": score,
#         "step":[],
#         "date":date,
#         "status":"True"
#     })
#     setConfig(data)

# def todoAddStep(uid,stepid,step):
#     """
#     给指定 uid 的 todo 项添加一个步骤字符串
#     """
#     data = getConfig()
#     todo_list = data.get("TODO", [])
    
#     # 查找对应 uid
#     for item in todo_list:
#         if item["uid"] == uid:
#             # 确保 item 有 step 列表
#             if "step" not in item or not isinstance(item["step"], list):
#                 item["step"] = []
#             item["step"].append([stepid,step,"False"])
#             setConfig(data)  # 保存更新
#             return  # 添加完成后返回
    
#     # 如果没有找到对应 uid
#     raise ValueError(f"TODO uid={uid} 不存在")

# def getTodoStep(uid):
#     """
#     给指定 uid 的 todo 项添加一个步骤字符串
#     """
#     data = getConfig()
#     todo_list = data.get("TODO", [])
    
#     # 查找对应 uid
#     for item in todo_list:
#         if item["uid"] == uid:
#             # 确保 item 有 step 列表
#             return item["step"] # 添加完成后返回
    
#     # 如果没有找到对应 uid
#     raise ValueError(f"TODO uid={uid} 不存在")

# def setTodoStep(uid,stepid,stat):
#     """
#     给指定 uid 的 todo 项添加一个步骤字符串
#     """
#     data = getConfig()
#     todo_list = data.get("TODO", [])
    
#     # 查找对应 uid
#     for item in todo_list:
#         if item["uid"] == uid:
#             # 确保 item 有 step 列表
#             # print(item["step"][stepIndex])
#             for i,tmp in enumerate(item["step"]):
#                 if tmp[0]==stepid:
#                     item["step"][i][2]=stat
#                     setConfig(data)
#                     return
#     # 如果没有找到对应 uid
#     raise ValueError(f"TODO uid={uid} 不存在")

# def delTodoStep(uid,stepid):
#     """
#     给指定 uid 的 todo 项添加一个步骤字符串
#     """
#     data = getConfig()
#     todo_list = data.get("TODO", [])
    
#     # 查找对应 uid
#     for item in todo_list:
#         if item["uid"] == uid:
#             # 确保 item 有 step 列表
#             for tmp in item["step"]:
#                 if tmp[0]==stepid:
#                     item["step"].remove(tmp)
#                     setConfig(data)
#                     return
    
#     # 如果没有找到对应 uid
#     raise ValueError(f"TODO uid={uid} 不存在")

# def removeTodo(uid):
#     data = getConfig()
#     before = len(data.get("TODO", []))
#     data["TODO"] = [c for c in data.get("TODO", []) if c["uid"] != uid]
#     if len(data["TODO"]) == before:
#         raise ValueError(f"{uid} 不存在")
#     setConfig(data)