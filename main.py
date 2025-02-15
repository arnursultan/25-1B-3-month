import asyncio
import logging
from logging import basicConfig
from bot import bot, dp
from handlers import start, help, menu, echo

async def main():
    logging.basicConfig(level=logging.INFO)

    dp.include_router(start.router)
    dp.include_router(help.router)
    dp.include_router(menu.router)
    dp.include_router(echo.router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())