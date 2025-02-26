import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import news

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(news.router)

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