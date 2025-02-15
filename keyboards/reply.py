from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=" Найти"), KeyboardButton(text=" О нас")],
        [KeyboardButton(text=" Контакты"), KeyboardButton(text=" Помощь")]
    ],
    resize_keyboard = True
)

__all__ = ["menu_keyboard"]