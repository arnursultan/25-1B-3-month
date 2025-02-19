from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS
from databases import get_all_users, delete_user

router = Router()

@router.message(Command("list_users"))
async def list_users(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для использования этой команды!")
        return

    users = get_all_users()
    if not users:
        await message.answer("В базе данных пока нет пользователей.")
        return

    text = "\n".join([f"ID={user_id}: {fullname}, {age} лет" for user_id, fullname, age in users])
    await message.answer(f"Список пользователей:\n{text}")

@router.message(Command("remove_user"))
async def remove_user(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для использования этой команды!")
        return

    users = get_all_users()
    if not users:
        await message.answer("Нет пользователей дял удаления.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=f"Удалить {user_id}. {fullname} ({age} лет)",
                              callback_data="remove_user_{user_id}")]
        for user_id, fullname, age in users
    ])

    await message.answer("Выберите пользователя, которого хотите удалить:", reply_markup=kb)

@router.callback_query(lambda c: c.data.startswith("remove_user_"))
async def remove_user_callback(callback: types.CallbackQuery):
    user_id = int(callback.data.split("_")[-1])
    delete_user(user_id)
    await callback.message.edit_text(f"Пользователь с ID={user_id} удален.")
    await callback.answer()

def register_handlers(dp):
    dp.include_router(router)