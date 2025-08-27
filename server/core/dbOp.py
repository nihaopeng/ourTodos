# ========== 数据库初始化 ==========
import sqlite3

DB_PATH = "todos.db"

def init_db():
    conn = connect()
    c = conn.cursor()

    # users
    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
      email TEXT PRIMARY KEY,
      username   TEXT,
      password   TEXT,
      score      INTEGER DEFAULT 0,
      profile    TEXT
    );""")

    # todos
    c.execute("""
    CREATE TABLE IF NOT EXISTS todos(
      todoid     INTEGER PRIMARY KEY AUTOINCREMENT,
      content    TEXT,
      describe   TEXT,
      ddl        TEXT,
      score      INTEGER DEFAULT 0,
      email TEXT REFERENCES users(email) ON DELETE CASCADE
    );""")

    # steps（带外键，级联删除）
    c.execute("""
    CREATE TABLE IF NOT EXISTS steps(
      stepid   INTEGER PRIMARY KEY AUTOINCREMENT,
      stepName TEXT,
      status   TEXT,
      todoid   INTEGER NOT NULL,
      FOREIGN KEY(todoid) REFERENCES todos(todoid) ON DELETE CASCADE
    );""")

    conn.commit()
    conn.close()

# ========== 工具函数 ==========
def connect():
    conn = sqlite3.connect(DB_PATH)
    # 开启外键（对每个连接都要做）
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def query_db(sql, args=(), one=False):
    conn = connect()
    cur = conn.cursor()
    cur.execute(sql, args)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    return (rows[0] if rows else None) if one else rows