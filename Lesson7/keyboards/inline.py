from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Наш сайт', url="https://geeks.kg")],
        [InlineKeyboardButton(text='Поддержка', url="https://t.me/ar_nursultan")]
    ]
)