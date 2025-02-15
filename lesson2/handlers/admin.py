from aiogram import types, Dispatcher
from aiogram.filters import Command
from config import ADMIN_ID

def register_admin_handlers(dp: Dispatcher):

    @dp.message(Command("admin"))
    async def admin_start(message: types.Message):
        if message.from_userd.id == ADMIN_ID:
            await message.reply("Привет, админ! Используй /ban, /unban и /banned_users для управления пользователями.")
        else:
            await message.reply("У вас нет доступа к этой команде.")

    @dp.message(Command("ban"))
    async def ban_user(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            await message.reply("У вас нет доступа к этой команде.")
            return

        try:
            user_id = int(message.text.split()[1])
            dp["banned_users"].add(user_id)
            await message.reply(f"Пользователь {user_id} заблокирован.")
        except (IndexError, ValueError):
            await message.reply("Используйте команду в формате: /ban <user_id>")

    @dp.message(Command("unban"))
    async def unban_user(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            await message.reply("У вас нет доступа к этой команде.")
            return

        try:
            user_id = int(message.text.split()[1])
            dp["banned_users"].discard(user_id)
            await message.reply(f"Пользователь {user_id} разблокирован.")
        except (IndexError, ValueError):
            await message.reply("Используйте команду в формате: /unban <user_id>")

    @dp.message(Command("banned_users"))
    async def list_banned_users(message: types.Message):
        if message.from_user.id != ADMIN_ID:
            await message.reply("У вас нет доступа к этой команде.")
            return

        banned_users = dp.get("banned_users", set())
        if banned_users:
            users_list = "\n".join(str(user) for user in banned_users)
            await message.reply(f"Заблокированные пользователи:\n{users_list}")
        else:
            await message.reply("Нет заблокированных пользователей.")

