from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.inline import info_keyboard

router = Router()

@router.message(Command("info"))
@router.message(F.text == "ℹ Инфо")
async def info_command(message: Message):
    await message.answer("ℹ Я многофункциональный бот! Подробнее:", reply_markup=info_keyboard)
