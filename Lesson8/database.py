import sqlite3

conn = sqlite3.connect("bot_course.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        progress INTEGER DEFAULT 0
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question TEXT NOT NULL,
        answer TEXT NOT NULL
    )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_answers (
        user_id INTEGER,
        question_id INTEGER,
        user_answer TEXT,
        correct_answer TEXT,
        FOREIGN KEY (user_id) REFERENCES users (user_id),
        FOREIGN KEY (question_id) REFERENCES questions (id)
    )
''')

conn.commit()

def add_user(user_id, username):
    try:
        cursor.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, username))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")

def get_progress(user_id):
    cursor.execute("SELECT progress FROM users WHERE user_id=?", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else 0

def update_progress(user_id, new_progress):
    cursor.execute("UPDATE users SET progress=? WHERE user_id=?", (new_progress, user_id))
    conn.commit()

def add_question(question, answer):
    cursor.execute("INSERT INTO questions (question, answer) VALUES (?, ?)", (question, answer))
    conn.commit()

def delete_question(q_id):
    cursor.execute("DELETE FROM questions WHERE id=?", (q_id,))
    conn.commit()

def edit_question(q_id, new_question, new_answer):
    cursor.execute("UPDATE questions SET question=?, answer=? WHERE id=?", (new_question, new_answer, q_id))
    conn.commit()

def get_all_questions():
    cursor.execute("SELECT id, question FROM questions ORDER BY id")
    return cursor.fetchall()

def clear_all_questions():
    cursor.execute("DELETE FROM questions")
    conn.commit()

def get_question(q_id):
    cursor.execute("SELECT question FROM questions WHERE id=?", (q_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def check_answer(user_id, q_id, user_answer):
    cursor.execute("SELECT answer FROM questions WHERE id=?", (q_id,))
    row = cursor.fetchone()

    if row:
        correct_answer = row[0].strip().lower()
        user_answer = user_answer.strip().lower()

        if correct_answer == user_answer:
            return True
        else:
            cursor.execute('''
                INSERT INTO user_answers (user_id, question_id, user_answer, correct_answer)
                SELECT ?, ?, ?, ? WHERE NOT EXISTS (
                    SELECT 1 FROM user_answers WHERE user_id=? AND question_id=?
                )
            ''', (user_id, q_id, user_answer, correct_answer, user_id, q_id))
            conn.commit()
            return False
    return False

def count_questions():
    cursor.execute("SELECT COUNT(*) FROM questions")
    return cursor.fetchone()[0]

def get_student_errors(user_id):
    cursor.execute("SELECT question_id, user_answer, correct_answer FROM user_answers WHERE user_id=?", (user_id,))
    return cursor.fetchall()

def get_user_errors_count(user_id):
    cursor.execute("SELECT COUNT(*) FROM user_answers WHERE user_id=?", (user_id,))
    return cursor.fetchone()[0]

def get_statistics():
    cursor.execute("SELECT user_id, COUNT(question_id) FROM user_answers GROUP BY user_id")
    return cursor.fetchall()

def close_connection():
    conn.close()

def renumber_questions():
    cursor.execute("SELECT id FROM questions ORDER BY id")
    rows = cursor.fetchall()

    for new_id, (old_id,) in enumerate(rows, start=1):
        cursor.execute("UPDATE questions SET id = ? WHERE id = ?", (new_id, old_id))

    conn.commit()

