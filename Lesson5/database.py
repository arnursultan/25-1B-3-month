import sqlite3

conn = sqlite3.connect("bot_database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id INTEGER UNIQUE,
    name TEXT,
    latitude REAL,
    longitude REAL,
    schedule_time TEXT
)
""")
conn.commit()

def add_user(chat_id, name, latitude, longitude):
    cursor.execute("""
        INSERT INTO users (chat_id, name, latitude, longitude)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(chat_id) DO UPDATE SET name=excluded.name, latitude=excluded.latitude, longitude=excluded.longitude
    """, (chat_id, name, latitude, longitude))
    conn.commit()

def update_schedule(chat_id, schedule_time):
    cursor.execute("UPDATE users SET schedule_time = ? WHERE chat_id = ?", (schedule_time, chat_id))
    conn.commit()

def get_scheduled_users():
    cursor.execute("SELECT chat_id, schedule_time FROM users WHERE schedule_time IS NOT NULL")
    return cursor.fetchall()

def get_all_users():
    cursor.execute("SELECT chat_id, name, latitude, longitude FROM users")
    return cursor.fetchall()
