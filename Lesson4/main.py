import asyncio
import logging
from aiogram import Bot, Dispatcher, fsm
from config import BOT_TOKEN
from config import bot, dp
from databases import init_db
from handlers import start, admin, fsm_admin

logging.basicConfig(level=logging.INFO)

async def main():
    init_db()

    start.register_handlers(dp)
    admin.register_handlers(dp)
    fsm_admin.register_handlers(dp)

    print("Бот запущен!")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        print("Бот завершил работу!")

if __name__ == "__main__":
    asyncio.run(main())

