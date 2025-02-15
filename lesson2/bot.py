# Lesson2/
#     bot.py            # Главный файл для запуска бота
#     config.py         # Конфигурации( токен, ID администратора)
#     handlers
#         admin.py      # Команды и функции для администратора
#         user.py       # Команды и функции для пользователей
#     .env              # Переменные окружения(токен и ID администратора)



from aiogram import Bot, Dispatcher
import asyncio
from config import BOT_TOKEN
from handlers import admin, user

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

dp["banned_users"] = set()

admin.register_admin_handlers(dp)
user.register_user_handlers(dp)

async def main():
    print("Бот запущен!")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        print("Бот завершил работу!")

if __name__ == '__main__':
    asyncio.run(main())