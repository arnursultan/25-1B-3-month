from aiogram import Router, types
from aiogram.filters import Command
from keyboards.reply import menu_keyboard

router = Router()

@router.message(Command("menu"))
async def menu_handler(message: types.Message):
    await message.answer("Главное меню:", reply_markup=menu_keyboard)
