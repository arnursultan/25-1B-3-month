import requests
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import WEATHER_API_KEY

router = Router()


class WeatherState(StatesGroup):
    waiting_for_city = State()


@router.message(Command("weather"))
@router.message(F.text == "🌦 Погода")
async def ask_city(message: Message, state: FSMContext):
    await message.answer("🌍 Введите название города для получения погоды:")
    await state.set_state(WeatherState.waiting_for_city)


@router.message(WeatherState.waiting_for_city, F.text)
async def get_weather(message: Message, state: FSMContext):
    city = message.text.strip()

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=ru"

    response = requests.get(url).json()

    if response.get("main"):
        temp = response["main"]["temp"]
        feels_like = response["main"]["feels_like"]
        weather_desc = response["weather"][0]["description"].capitalize()
        humidity = response["main"]["humidity"]
        wind_speed = response["wind"]["speed"]

        weather_info = (
            f"🌤 Погода в {city}:\n"
            f"🌡 Температура: {temp}°C\n"
            f"🤒 Ощущается как: {feels_like}°C\n"
            f"💨 Ветер: {wind_speed} м/с\n"
            f"💧 Влажность: {humidity}%\n"
            f"☁️ {weather_desc}"
        )

        await message.answer(weather_info)
    else:
        await message.answer("❌ Ошибка! Город не найден. Попробуйте ещё раз.")

    await state.clear()
