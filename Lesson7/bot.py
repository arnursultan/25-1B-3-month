from aiogram import Bot, Dispatcher
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from middlewares.logger import LoggerMiddleware
from middlewares.throttling import ThrottlingMiddleware
from handlers import start, admin, info, weather
# import database

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.message.middleware(LoggerMiddleware())
dp.message.middleware(ThrottlingMiddleware(5))

dp.include_router(start.router)
dp.include_router(admin.router)
dp.include_router(info.router)
dp.include_router(weather.router)
# dp.include_router(feedback.router)

async def main():
    print("Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        print("Бот завершил работу!")


if __name__ == "__main__":
    asyncio.run(main())