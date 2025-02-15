from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Router
from databases import save_feedback

router = Router()

class FeedbackForm(StatesGroup):
    name = State()
    email = State()
    message = State()

@router.message(Command("feedback"))
async def start_feedback(message: types.Message, state: FSMContext):
    await message.answer("Введите ваше имя: ")
    await state.set_state(FeedbackForm.name)

@router.message(FeedbackForm.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите ваш email: ")
    await state.set_state(FeedbackForm.email)

@router.message(FeedbackForm.email)
async def process_email(message: types.Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Введите ваше сообщение: ")
    await state.set_state(FeedbackForm.message)

@router.message(FeedbackForm.message)
async def process_message(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await save_feedback(message.from_user.id, data["name"], data["email"], message.text)
    await message.answer("Спасибо за ваш отзыв! Данные сохранены.")
    await state.clear()