from aiogram import types, Router
from aiogram.filters import Command
from config import ADMIN_IDS

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id in ADMIN_IDS:
        await message.answer(
            "Привет, администратор!\n\n"
            "Доступные команды:\n"
            "/add_user — добавить нового пользователя\n"
            "/list_users — показать всех пользователей\n"
            "/remove_user — удалить пользователя\n"
            "/edit_user — редактировать пользователя\n"
        )
    else:
        await message.answer(
            "Привет! Я бот.\n"
            "Пока что у меня нет команд для обычных пользователей.\n"
            "Обратитесь к администратору, если нужен доступ."
        )

def register_handlers(dp):
    dp.include_router(router)
