# ========== 用户相关接口 ==========
import random
import string
import time
from flask import jsonify, request, Blueprint
from core.dbOp import query_db
from flask import request, jsonify, session
from flask_mail import Mail, Message
from functools import wraps
# from main import query_db
# 配置邮件服务器
mail = Mail()

userViewBp = Blueprint("userView",__name__)

verification_codes = {}

CODE_EXPIRY_TIME = 300  # 5分钟

# ========== 发送验证码 ========== 
@userViewBp.route("/send_verification_code", methods=["POST"])
def send_verification_code():
    data = request.get_json()
    email = data.get("email")

    # 生成验证码（6位数字字母混合）
    code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    verification_codes[email] = (time.time(), code)

    # 邮件内容
    # print(email)
    msg = Message('Your Verification Code', recipients=[email])
    msg.body = f"Your verification code is {code}."

    try:
        mail.send(msg)
        return jsonify({"code": 200, "msg": "Verification code sent successfully."})
    except Exception as e:
        return jsonify({"code": 500, "msg": str(e)})

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        data = request.get_json()
        email = data.get("email")
        print(session.get("email"),email)
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
        return jsonify({"code": 200, "msg": "ok","username":user[1]})
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
    verification_code = data.get("code")

    # 验证验证码
    if email not in verification_codes:
        return jsonify({"code": 401, "msg": "Verification code not sent."})

    created_time, code = verification_codes[email]
    
    if time.time() - created_time > CODE_EXPIRY_TIME:
        return jsonify({"code": 401, "msg": "Verification code expired."})
    
    if code != verification_code:
        return jsonify({"code": 401, "msg": "Invalid verification code."})

    # 检查新用户名是否已存在
    exists = query_db("SELECT * FROM users WHERE username=?", (username,), one=True)
    if exists:
        return jsonify({"code": 401, "msg": "Username already exists."})

    # 查重
    exists = query_db("SELECT * FROM users WHERE email=?", (email,), one=True)
    if exists:
        return jsonify({"code": 401, "msg": "Email already exists."})

    # 插入新用户
    query_db("INSERT INTO users (email, username, password, score, profile) VALUES (?,?,?,?,?)",
             (email, username, password, 0, ""))
    
    # 成功注册后，移除已使用的验证码
    del verification_codes[email]

    return jsonify({"code": 200, "msg": "Registration successful."})

# 修改用户名和密码
@userViewBp.route("/update_username_and_password", methods=["POST"])
@login_required
def update_username():
    data = request.get_json()
    email = data.get("email")
    new_username = data.get("username")
    new_password = data.get("password")

    # 检查新用户名是否已存在
    exists = query_db("SELECT * FROM users WHERE username=?", (email,), one=True)
    if exists:
        return jsonify({"code": 401, "msg": "Username already exists."})

    query_db("UPDATE users SET username=? WHERE email=?", (new_username, email))
    query_db("UPDATE users SET password=? WHERE email=?", (new_password, email))
    return jsonify({"code": 200, "msg": "Username updated successfully."})

@userViewBp.route("/set_profile", methods=["POST"])
@login_required
def set_profile():
    data = request.get_json()
    email = data.get("email")
    profile = data.get("profile")

    query_db("UPDATE users SET profile=? WHERE email=?", (profile, email))
    return jsonify({"code": 200, "msg": "profile updated successfully."})

@userViewBp.route("/get_profile", methods=["POST"])
@login_required
def get_profile():
    data = request.get_json()
    email = data.get("email")
    profile = query_db("SELECT profile FROM users WHERE email=?", (email,), one=True)
    if profile:
        return jsonify({"code": 200, "profile": profile[0]})
    return jsonify({"code": 404, "msg": "user not found"})

# ========== 积分相关接口 ==========
@userViewBp.route("/get_user_score", methods=["POST"])
@login_required
def get_user_score_view():
    data = request.get_json()
    email = data.get("email")
    score = query_db("SELECT score FROM users WHERE email=?", (email,), one=True)
    if score:
        return jsonify({"code": 200, "score": score[0]})
    return jsonify({"code": 404, "msg": "user not found"})

@userViewBp.route("/get_scores", methods=["POST"])
@login_required
def get_scores_view():
    users = query_db("SELECT email, username, score FROM users")
    results = [{"email": u[0], "username": u[1], "score": u[2]} for u in users]
    return jsonify({"code": 200, "data": results})