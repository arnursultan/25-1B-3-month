import sqlite3
from contextlib import closing

DB_PATH = "bot_db.sqlite3"

def init_db():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fullname TEXT NOT NULL,
                    age INTEGER NOT NULL
                );
            """)

def add_user(fullname: str, age: int):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("INSERT INTO users (fullname, age) VALUES (?, ?)", (fullname, age))

def get_all_users():
    with closing(sqlite3.connect(DB_PATH)) as conn:
        return conn.execute("SELECT user_id, fullname, age FROM users").fetchall()

def get_user_by_id(user_id: int):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        return conn.execute("SELECT user_id, fullname, age FROM users WHERE user_id = ?", (user_id,)).fetchone()

def update_user(user_id: int, fullname: str, age: int):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("UPDATE users SET fullname = ?, age = ? WHERE user_id = ?", (fullname, age, user_id))

def delete_user(user_id: int):
    with closing(sqlite3.connect(DB_PATH)) as conn:
        with conn:
            conn.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
