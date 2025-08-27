# ========== 用户相关接口 ==========
from flask import jsonify, request, Blueprint
from core.dbOp import query_db
from flask import Flask, request, jsonify, session
from functools import wraps
# from main import query_db

userViewBp = Blueprint("userView",__name__)

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json()
        email = data.get("email")
        # print(session.get("email"),email)
        if session.get("email")!=email:
            return jsonify({"code": 401, "msg": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated

@userViewBp.route("/login", methods=["POST"])
def login_view():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = query_db("SELECT * FROM users WHERE email=? AND password=?", (email, password), one=True)
    if user:
        session["email"] = email
        return jsonify({"code": 200, "msg": "ok"})
    return jsonify({"code": 401, "msg": "wrong account/password"})

# 登出接口
@userViewBp.route("/logout", methods=["POST"])
@login_required
def logout():
    session.pop("email", None)
    return jsonify({"code": 200, "msg": "logout"})

@userViewBp.route("/regist", methods=["POST"])
def regist_view():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    # 查重
    exists = query_db("SELECT * FROM users WHERE email=?", (email,), one=True)
    if exists:
        return jsonify({"code": 401, "msg": "wrong/repeat"})

    query_db("INSERT INTO users (email, username, password, score, profile) VALUES (?,?,?,?,?)",
             (email, username, password, 0, ""))
    return jsonify({"code": 200, "msg": "ok"})

# ========== 积分相关接口 ==========
@userViewBp.route("/get_user_score", methods=["POST"])
@login_required
def get_user_score_view():
    data = request.get_json()
    email = data.get("email")
    score = query_db("SELECT score FROM users WHERE email=?", (email,), one=True)
    if score:
        return jsonify({"code": 200, "score": score})
    return jsonify({"code": 404, "msg": "user not found"})

@userViewBp.route("/get_scores", methods=["GET"])
@login_required
def get_scores_view():
    users = query_db("SELECT email, username, score FROM users")
    results = [{"email": u[0], "username": u[1], "score": u[2]} for u in users]
    return jsonify({"code": 200, "data": results})