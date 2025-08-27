from flask import Flask
import os
from core.userView import userViewBp
from core.todo import todoViewbp
from core.dbOp import DB_PATH,init_db

app = Flask(__name__)
app.secret_key = "my_secret_key"   # 必须设置，用于签名 cookie

app.register_blueprint(userViewBp)
app.register_blueprint(todoViewbp)

# ========== 主入口 ==========
if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
