import asyncio
import logging
import schedule
import math
import re
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from database import add_user, update_schedule, get_scheduled_users, get_all_users
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=" Отправить локацию", request_location=True)],
        [KeyboardButton(text=" Найти ближайшего пользователя")],
        [KeyboardButton(text=" Установить расписание рассылки")],
    ],
    resize_keyboard=True
)

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        f"Привет, {message.from_user.full_name}!  Чтобы зарегистрироваться, отправьте свою геолокацию, нажав на кнопку ниже.",
        reply_markup=menu
    )

@dp.message(lambda msg: msg.location is not None)
async def location_handler(message: Message):
    chat_id = message.chat.id
    name = message.from_user.full_name
    latitude = message.location.latitude
    longitude = message.location.longitude

    add_user(chat_id, name, latitude, longitude)

    await message.answer(" Ваша локация сохранена! Теперь вы можете искать ближайших пользователей.", reply_markup=menu)

@dp.message(lambda msg: msg.text == " Найти ближайшего пользователя")
async def nearest_user(message: Message):
    users = get_all_users()
    chat_id = message.chat.id

    my_user = next((user for user in users if user[0] == chat_id), None)

    if not my_user:
        await message.answer(" Вы еще не зарегистрированы! Отправьте вашу локацию через /start.")
        return

    my_lat, my_lon = my_user[2], my_user[3]

    if len(users) < 2:
        await message.answer(" В базе данных пока нет других пользователей.")
        return

    other_users = [user for user in users if user[0] != chat_id]

    closest_user = min(other_users, key=lambda user: haversine(my_lat, my_lon, user[2], user[3]))

    await message.answer(
        f" Ближайший пользователь: {closest_user[1]} (ID: {closest_user[0]})\n"
        f" Расстояние: {haversine(my_lat, my_lon, closest_user[2], closest_user[3]):.2f} км"
    )

@dp.message(lambda msg: msg.text == " Установить расписание рассылки")
async def set_schedule(message: Message):
    await message.answer(" Введите время в формате HH:MM (например, 10:00)")

@dp.message()
async def receive_schedule_time(message: Message):
    if re.match(r"^\d{2}:\d{2}$", message.text):
        update_schedule(message.chat.id, message.text)
        await message.answer(f" Ваше расписание установлено на {message.text}!")
    else:
        await message.answer(" Формат времени неверный. Введите в формате HH:MM.")

async def send_message_task(chat_id):
    try:
        await bot.send_message(chat_id, " Напоминание: Время выполнять задачи!")
    except Exception as e:
        logging.error(f"Ошибка при отправке сообщения пользователю {chat_id}: {e}")

def run_send_message_task(chat_id):
    asyncio.create_task(send_message_task(chat_id))

async def schedule_messages():
    users = get_scheduled_users()
    if not users:
        logging.info("Нет пользователей с установленным расписанием.")
    else:
        for chat_id, schedule_time in users:
            schedule.every().day.at(schedule_time).do(run_send_message_task, chat_id)

async def send_scheduled_messages():
    while True:
        await schedule_messages()
        schedule.run_pending()
        await asyncio.sleep(1)

async def main():
    asyncio.create_task(send_scheduled_messages())
    print("Бот запущен!")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        print("Бот завершил работу!")

if __name__ == "__main__":
    asyncio.run(main())
