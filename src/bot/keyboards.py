from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from database.crud import CRUDProgram

main_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Зарегестрироваться", callback_data="rega")],
    ]
)

servise_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать учебный план", callback_data="plan")],
    ]
)

choice_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Оформить подписку", callback_data="month")],
        [InlineKeyboardButton(text="Оплатить сразу весь курс ", callback_data="all_pay")],
    ]
)


def get_plans_menu_ikbd():
    programs = CRUDProgram.get_all()
    inline_keyboard = list()
    for program in programs:
        inline_keyboard.append(
            [InlineKeyboardButton(text=program.title, callback_data=str(program.num))]
        )
    plans_menu_ikbd = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return plans_menu_ikbd


def get_dop_plans_menu_ikbd():
    programs = CRUDProgram.get_all()
    inline_keyboard = list()
    for program in programs:
        inline_keyboard.append(
            [InlineKeyboardButton(text=program.title, callback_data=str(program.num))]
        )
    inline_keyboard.append([InlineKeyboardButton(text="Назад", callback_data="nazad")])
    dop_plans_menu_ikbd = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return dop_plans_menu_ikbd


select_plans_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать еще один план обучения", callback_data="dop_plan")],
        [InlineKeyboardButton(text="Завершить оплату и регистрацию", callback_data="quit")],
    ]
)

main_menu_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Выбрать дополнительные планы обучения")],
    ],
    resize_keyboard=True,
)
