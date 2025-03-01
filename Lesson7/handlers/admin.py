from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from filters.is_admin import IsAdmin

router = Router()

@router.message(IsAdmin(), Command("admin"))
@router.message(IsAdmin(), F.text == "🎛 Админ-панель")
async def admin_panel(message: Message):
    await message.answer("Привет, админ! Это твоя панель управления.")

@router.message(IsAdmin(), Command("stats"))
async def stats(message: Message):
    await message.answer("📊 Бот работает стабильно. Количество пользователей: 100.")
