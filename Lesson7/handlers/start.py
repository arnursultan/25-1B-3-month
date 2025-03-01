from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.reply import main_keyboard

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Я многофункциональный бот. Выберите действие:", reply_markup=main_keyboard)

@router.message(Command("help"))
async def help_command(message: Message):
        help_text = (
            "📝 Доступные команды:\n"
            "/start - Запуск бота\n"
            "/help - Список команд\n"
            "/admin - Панель администратора\n"
            "/stats - Статистика бота\n"
            "/info - О боте\n"
            "/weather - Узнать погоду\n"
            "/feedback - Оставить отзыв"
        )
        await message.answer(help_text, reply_markup=main_keyboard)