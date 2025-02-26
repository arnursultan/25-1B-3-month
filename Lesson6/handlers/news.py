from time import strftime
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from parser import get_news
from datetime import datetime

router = Router()

@router.message(Command("news"))
async def send_news(message: types.Message):
    news = get_news("https://habr.com/ru/articles/")

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=" Открыть Habr", url="https://habr.com/ru/news/")],
        [InlineKeyboardButton(text=" Обновить", callback_data="update_news")]
    ])

    await message.answer(news, reply_markup=keyboard)

@router.callback_query(lambda c: c.data == "update_news")
async def update_news(callback: types.CallbackQuery):
    news = get_news("https://habr.com/ru/articles/")
    time_now = datetime.now().strftime("%H:%M:%S")

    new_text = f"{news}\n\n Обновлено в {time_now}"

    await callback.message.edit_text(new_text, reply_markup=callback.message.reply_markup)