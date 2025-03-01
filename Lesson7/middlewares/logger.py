from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(message)s')

class LoggerMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        logging.info(f"Пользователь {event.from_user.id} написал: {event.text}")
        return await handler(event, data)
