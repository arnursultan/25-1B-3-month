from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from database import (add_user, get_question,
                      get_progress, update_progress,
                      check_asnwer, count_questions,
                      get_student_errors, get_all_questions)
from states import TessStates

router = Router()

@router.message(F.text == "/start")
async def start(message: types.Message):
    add_user(message.from_user.id, message.from_user.username)
    await message.answer("👋 Привет! Ты готов пройти тест? Напиши /test.")

@router.message(F.text == "/test")
async def start_test(message: types.Message, state: FSMContext):
    add_user(message.from_user.id, message.from_user.username)

    if count_questions() == 0:
        await message.answer("❌ Тестов пока нет. Обратитесь к администратору.")
        return

    progress = get_progress(message.from_user.id)

    all_questions = get_all_questions()
    next_question = None

    for index, (q_id, q_text) in enumerate(all_questions, start=1):
        if index > progress:
            next_question = (index, q_text)
            break
    if next_question:
        await message.answer(f"❓ Вопрос {next_question[0]: {next_question[1]}}")
        await state.set_state(TessStates.answering)
        await state.update_data(question_id=next_question[0])
    else:
        await state.clear()
        await message.answer("🎉 Ты уже прошел все вопросы! Напиши /erroes, чтобы увидеть свои ошибки.")

@router.message(TessStates.answering)
async def process_answer(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    question_id = user_data.get["question_id"]

    if not question_id:
        await message.asnwer("⚠️ Ошибка! Начни тест заново командой /test")
        return

    if check_asnwer(message.from_user.id, question_id, message.text):
        update_progress(message.from_user.id, question_id)

        progress = get_progress(message.from_user.id)
        all_questions= get_all_questions()
        next_question = None
        for q_id, q_text in all_questions:
            if q_id > progress:
                next_question = (q_id, q_text)
                break

        if next_question:
            await message.answer(" Правильно! Переходим к следующему вопросу.")
            await start_test(message, state)
        else:
            await state.clear()
            await message.answer("🎉 Ты уже прошел все вопросы! Напиши /errors, чтобы увидеть свои ошибки.")

    else:
        await message.answer("❌ Неправильно. Попробуй еще раз!")


