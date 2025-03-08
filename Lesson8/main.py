import asyncio
import logging
import sys
from config import bot, dp
from handlers import student, admin
from aiogram.types import BotCommand


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout)
    ]
)

dp.include_router(student.router)
dp.include_router(admin.router)

async def main():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запуск бота"),
        BotCommand(command="test", description="Начать тест"),
        BotCommand(command="errors", description="Посмотреть ошибки"),
        BotCommand(command="add_question", description="Добавить вопрос"),
        BotCommand(command="edit_question", description="Изменить вопрос"),
        BotCommand(command="list_questions", description="Все вопросы (админ)"),
        BotCommand(command="delete_question", description="Удалить вопрос (админ)"),
        BotCommand(command="clear_questions", description="Очистить вопросы (админ)"),
        BotCommand(command="stats", description="Статистика (админ)")
    ])

    try:
        logging.info("✅ Бот запущен...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка во время работы бота: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logging.info("🛑 Бот завершил работу.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен вручную (Ctrl + C).")
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}", exc_info=True)
    finally:
        logging.info("🛑 Завершение работы бота.")