from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🌦 Погода"), KeyboardButton(text="ℹ Инфо")],
        [KeyboardButton(text="✍ Оставить отзыв"), KeyboardButton(text="🎛 Админ-панель")],
        [KeyboardButton(text="📜 Все отзывы")]
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Выберите действие..."
)
