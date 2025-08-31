from flask import Flask
import os
from core.userView import userViewBp,mail
from core.todo import todoViewbp
from core.dbOp import DB_PATH,init_db

app = Flask(__name__)
app.secret_key = "my_secret_key"   # 必须设置，用于签名 cookie
app.config['MAIL_SERVER'] = 'smtp.qq.com'  # 你的邮件服务器地址
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'YutaoPeng@foxmail.com'
app.config['MAIL_PASSWORD'] = 'payxyobhulfwchce'
mail.init_app(app)

app.register_blueprint(userViewBp)
app.register_blueprint(todoViewbp)

# ========== 主入口 ==========
if __name__ == "__main__":
    if not os.path.exists(DB_PATH):
        init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
