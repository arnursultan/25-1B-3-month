from aiogram import types
from aiogram.filters import Command
from aiogram.fsm.context import  FSMContext
from aiogram import Router

router = Router()

@router.message(Command('start'))
async def cmf_start(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет! Я бот для сбора обратной связи. Используй /feedback, чтобы оставить отзыв.")
