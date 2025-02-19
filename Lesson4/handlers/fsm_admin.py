from aiogram import types, Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import ADMIN_IDS
from databases import add_user, update_user, get_all_users, get_user_by_id
from states import FSMAdminAdd, FSMAdminEdit


router = Router()
@router.message(Command("add_user"))
async def start_add_user(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для использования этой команды!")
        return

    await message.answer("Введите полное имя пользователя:")
    await state.set_state(FSMAdminAdd.fullname)

@router.message(FSMAdminAdd.fullname)
async def load_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Введите возраст пользователя:")
    await state.set_state(FSMAdminAdd.age)

@router.message(FSMAdminAdd.age)
async def load_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Пожалуйста, введите число (возраст).")
        return

    age = int(message.text)
    data = await state.get_data()
    fullname = data.get("fullname")

    add_user(fullname, age)
    await message.answer(f"Пользователь '{fullname}' (возраст: {age}) успешно добавлен!")
    await state.clear()

@router.message(Command("edit_user"))
async def start_edit_user(message: types.Message, state: FSMContext):
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("У вас нет прав для использования этой команды!")
        return

    users = get_all_users()
    if not users:
        await message.answer("В базе данных нет пользователей для редактирования.")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text=f"{user_id}. {fullname} ({age} лет)",
            callback_data=f"edit_user_{user_id}"
        )] for user_id, fullname, age in users
    ])

    await message.answer("Выберите пользователя для редактирования:", reply_markup=kb)
    await state.set_state(FSMAdminEdit.choose_user)


@router.callback_query(lambda c: c.data.startswith("edit_user_"))
async def edit_user_callback(callback_query: types.CallbackQuery, state: FSMContext):
    user_id_str = callback_query.data.split("_")[-1]
    user_id = int(user_id_str)

    await state.update_data(user_id=user_id)
    await callback_query.message.answer("Введите новое полное имя пользователя:")
    await state.set_state(FSMAdminEdit.edit_fullname)
    await callback_query.answer()


@router.message(FSMAdminEdit.edit_fullname)
async def edit_fullname(message: types.Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Введите новый возраст:")
    await state.set_state(FSMAdminEdit.edit_age)


@router.message(FSMAdminEdit.edit_age)
async def edit_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Возраст должен быть числом! Повторите ввод /edit_user.")
        await state.clear()
        return

    age = int(message.text)
    data = await state.get_data()

    user_id = data.get("user_id")
    new_fullname = data.get("fullname")

    update_user(user_id, new_fullname, age)
    await message.answer(f"Данные пользователя (ID={user_id}) обновлены: '{new_fullname}', {age} лет.")
    await state.clear()

def register_handlers(dp):
    dp.include_router(router)

