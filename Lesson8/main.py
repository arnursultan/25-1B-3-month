import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from config import bot, dp

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("bot.log", encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]
)

async def main():

    try:
        logging.info("✅ Бот запущен...")
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"❌ Ошибка во время работы бота: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logging.info("🛑 Бот завершил работу.")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("🛑 Бот остановлен вручную (Ctrl + C.")
    except Exception as e:
        logging.error(f"❌ Критическая ошибка: {e}", exc_info=True)
    finally:
        logging.info("🛑 Завершение работы бота.")