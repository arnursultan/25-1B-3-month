import asyncio
from aiogram import BaseMiddleware
from aiogram.types import Message

class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, delay: int):
        self.delay = delay
        self.users = {}

    async def __call__(self, handler, event: Message, data: dict):
        user_id = event.from_user.id
        if user_id in self.users and self.users[user_id]:
            await event.answer("⏳ Подождите перед следующим запросом!")
            return
        self.users[user_id] = True
        await handler(event, data)
        await asyncio.sleep(self.delay)
        self.users[user_id] = False
