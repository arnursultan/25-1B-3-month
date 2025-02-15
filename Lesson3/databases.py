import aiosqlite

DB_NAME = "feedback.db"

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL
            )
        """)
        await db.commit()

async def save_feedback(telegram_id, name, email, message):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO feedback (telegram_id, name, email, message)
            VALUES (?, ?, ?, ?)
        """, (telegram_id, name, email, message))
        await db.commit()