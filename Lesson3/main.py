# from aiogram import Bot, Dispatcher
# from aiogram.fsm.storage.memory import MemoryStorage
# from aiogram.types import Message
# from aiogram.filters import Command
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.fsm.context import FSMContext
# from config import BOT_TOKEN
# import asyncio
# import aiosqlite
#
# bot = Bot(token=BOT_TOKEN)
# storage = MemoryStorage()
# dp = Dispatcher(storage=storage)
#
# class Form(StatesGroup):
#     name = State()
#     age = State()
#     confirmation = State()
#
# async def init_db():
#     async with aiosqlite.connect("bot_database.db") as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 telegram_id INTEGER NOT NULL,
#                 name TEXT NOT NULL,
#                 age INTEGER NOT NULL
#                 )
#         """)
#         await db.commit()
#
# @dp.message(Command('start'))
# async def cmd_start(message: Message, state: FSMContext):
#     await message.answer("Привет! Как вас зовут?")
#     await state.set_state(Form.name)
#
# @dp.message(Form.name)
# async def process_name(message: Message, state: FSMContext):
#     await state.update_data(name=message.text)
#     await message.answer("Сколько вам лет?")
#     await state.set_state(Form.age)
#
# @dp.message(Form.age)
# async def process_age(message: Message, state: FSMContext):
#     await state.update_data(age=message.text)
#     user_data = await state.get_data()
#     await message.answer(f"Вас зовут {user_data['name']} и вам {user_data['age']} лет. Все верно? (Да/нет)")
#     await state.set_state(Form.confirmation)
#
# @dp.message(Form.confirmation)
# async def process_confirmation(message: Message, state: FSMContext):
#     if message.text.lower() == "да":
#         user_data = await state.get_data()
#         async with aiosqlite.connect("bot_database.db") as db:
#             await db.execute("""
#                 INSERT INTO users (telegram_id, name, age) VALUES (?, ?, ?)
#             """, (message.from_user.id, user_data['name'], user_data['age']))
#             await db.commit()
#         await message.answer("Данные сохранены!")
#         await state.clear()
#     else:
#         await message.answer("Давайте попробуем снова. Как вас зовут?")
#         await state.set_state(Form.name)
#
# @dp.message(Command('upload'))
# async def cmf_upload(message: Message):
#     await bot.send_chat_action(message.chat.id, 'upload_document')
#     await asyncio.sleep(2)
#     await message.answer("Файл успешно загружен")
#
# async def main():
#     await init_db()
#     print("Бот запущен!")
#     try:
#         await dp.start_polling(bot)
#     except asyncio.CancelledError:
#         pass
#     finally:
#         print("Бот завершил работу!")
#
# if __name__ == '__main__':
#     asyncio.run(main())

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from databases import init_db
from handlers import start_router, feedback_router
import asyncio

async def main():
    await init_db()
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(start_router)
    dp.include_router(feedback_router)

    print("Бот запущен!")
    try:
        await dp.start_polling(bot)

    except asyncio.CancelledError:
        pass
    finally:
        print("Бот завершил работу!")

if __name__ == '__main__':
    asyncio.run(main())



