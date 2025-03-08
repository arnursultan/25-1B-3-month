from aiogram import Router, types, F
from database import (add_question, delete_question,
                      edit_question, get_statistics,
                      get_all_questions, clear_all_questions,
                      renumber_questions, get_question)
from config import ADMIN_ID

router = Router()

async def is_admin(message: types.Message) -> bool:
    return message.from_user.id == ADMIN_ID

# Добавление вопроса
@router.message(F.text.startswith("/add_question"))
async def add_new_question(message: types.Message):
    if not await is_admin(message):
        return

    parts = message.text.split(" - ")
    if len(parts) != 3:
        await message.answer("⚠️ Используйте формат: /add_question - Вопрос - Ответ")
        return

    question = parts[1].strip()
    answer = parts[2].strip()

    add_question(question, answer)
    await message.answer("✅ Вопрос добавлен!")

@router.message(F.text.startswith("/delete_question"))
async def remove_question(message: types.Message):
    if not await is_admin(message):
        return

    parts = message.text.split()
    if len(parts) != 2 or not parts[1].isdigit():
        await message.answer("⚠️ Используйте команду: /delete_question ID")
        return

    q_id = int(parts[1])
    delete_question(q_id)
    renumber_questions()

    await message.answer(f"✅ Вопрос {q_id} удален! ID обновлены.")

@router.message(F.text.startswith("/edit_question"))
async def modify_question(message: types.Message):
    if not await is_admin(message):
        return

    parts = message.text.split(" - ")

    if len(parts) != 4:
        await message.answer("⚠️ Используйте формат: /edit_question - ID - Новый вопрос - Новый ответ")
        return

    try:
        q_id = int(parts[1].strip())
    except ValueError:
        await message.answer("❌ Ошибка: ID должен быть числом!")
        return

    new_question = parts[2].strip()
    new_answer = parts[3].strip()

    question_exists = get_question(q_id)
    if not question_exists:
        await message.answer(f"❌ Ошибка: вопрос с ID {q_id} не существует!")
        return

    edit_question(q_id, new_question, new_answer)
    await message.answer(f"✅ Вопрос {q_id} отредактирован!")

@router.message(F.text == "/stats")
async def stats(message: types.Message):
    if not await is_admin(message):
        return

    stats = get_statistics()

    if not stats:
        await message.answer("📊 Пока никто не ошибался!")
        return

    report = "📊 <b>Статистика ошибок:</b>\n\n"
    for user_id, mistakes in stats:
        report += f"👤 Пользователь {user_id}: {mistakes} ошибок\n"

    await message.answer(report, parse_mode="HTML")

@router.message(F.text == "/list_questions")
async def list_questions(message: types.Message):
    if not await is_admin(message):
        return

    questions = get_all_questions()

    if not questions:
        await message.answer("📭 Вопросов пока нет.")
        return

    text = "📜 <b>Список всех вопросов:</b>\n\n"
    for q_id, question in questions:
        text += f"🔹 <b>ID {q_id}:</b> {question}\n"

    await message.answer(text, parse_mode="HTML")

@router.message(F.text == "/clear_questions")
async def clear_questions(message: types.Message):
    if not await is_admin(message):
        return

    clear_all_questions()
    await message.answer("✅ Все вопросы удалены.")
