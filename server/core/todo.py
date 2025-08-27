# ========== 待办事项接口 ==========
from flask import jsonify, request,Blueprint

from core.dbOp import query_db
from core.userView import login_required

todoViewbp = Blueprint('todoView',__name__)

@todoViewbp.route("/add_todo", methods=["POST"])
@login_required
def add_todo_view():
    data = request.get_json()
    name = data.get("todoName")
    desc = data.get("todoDescription")
    ddl = data.get("ddl")
    score = data.get("score", 0)
    email = data.get("email")

    query_db("INSERT INTO todos (content, describe, ddl, score, email) VALUES (?,?,?,?,?)",
             (name, desc, ddl, score, email))
    return jsonify({"code": 200, "msg": "ok"})


@todoViewbp.route("/del_todo", methods=["POST"])
@login_required
def del_todo_view():
    data = request.get_json()
    email = data.get("email")
    todo_id = data.get("todo_id")
    query_db("DELETE FROM todos WHERE todoid=? and email=?", (todo_id,email))
    return jsonify({"code": 200, "msg": "ok"})


@todoViewbp.route("/todo_complete", methods=["POST"])
@login_required
def todo_complete_view():
    data = request.get_json()
    todo_id = data.get("todo_id")
    # 这里只是简单标记完成，可以考虑加文件上传验证逻辑
    query_db("UPDATE todos SET score=score+10 WHERE todoid=?", (todo_id,))
    return jsonify({"code": 200, "msg": "ok"})

@todoViewbp.route("/step_change", methods=["POST"])
@login_required
def step_change_view():
    data = request.get_json()
    todo_id = data.get("todo_id")
    steps = data.get("steps", [])

    for step in steps:
        step_name = step["stepName"]
        status = step["status"]
        query_db("INSERT INTO steps (stepName, status, todoid) VALUES (?,?,?)",
                 (step_name, status, todo_id))
    return jsonify({"code": 200, "msg": "ok"})
