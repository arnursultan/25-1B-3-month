from aiogram.fsm.state import State, StatesGroup

class FSMAdminAdd(StatesGroup):
    fullname = State()
    age = State()

class FSMAdminEdit(StatesGroup):
    choose_user = State()
    edit_fullname = State()
    edit_age = State()