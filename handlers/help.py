from aiogram import Router, types
from aiogram.filters import Command

router = Router()

@router.message(Command("help"))
async def help_handler(message: types.Message):
    await message.answer(" Доступные команды:\n/start - Начало работы"
                         "\n/help - Помощь\n/menu - Главное меню")