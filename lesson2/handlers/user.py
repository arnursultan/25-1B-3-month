from aiogram import types, Dispatcher
from aiogram.filters import Command
from pyexpat.errors import messages


def register_user_handlers(dp: Dispatcher):
    @dp.message(Command("start"))
    async def start(message: types.Message):
        await message.reply("Привет! Я твой бот. Используй /help для списка команд.")

    @dp.message(Command("help"))
    async def help_command(message: types.Message):
        await message.reply("Доступные команды:\n/start - начать\n/help - помощь\n/info - Ваша информация")

    @dp.message(Command("info"))
    async def info_command(message: types.Message):
        user = message.from_user
        info = (
            f" Имя: {user.first_name}\n"
            f" Ваш ID: {user.id}\n"
            f" Юзернейм: @{user.username if user.username else 'нет'}\n"
        )
        await message.reply(info)

    @dp.message(Command("check"))
    async def check_ban(message: types.Message):
        banned_users = dp.get("banned_users", set())
        if message.from_user.id in banned_users:
            await message.reply("Вы заблокированы и не можете использовать бота.")
        else:
            await message.reply("Вы не заблокированы, добро пожаловать!")

