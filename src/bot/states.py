from aiogram.fsm.state import State, StatesGroup


class UserForm(StatesGroup):
    name = State()
    number = State()
    num = State()
    choice = State()
