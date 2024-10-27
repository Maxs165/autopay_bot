from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


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

plans_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Взрослое направление", callback_data="1")],
        [InlineKeyboardButton(text="Детское направление", callback_data="2")],
        [InlineKeyboardButton(text="Курс обучения моделей PLUS SIZE", callback_data="3")],
        [InlineKeyboardButton(text="Киноактерская группа", callback_data="4")],
        [InlineKeyboardButton(text="Агентский взнос", callback_data="5")],
    ]
)

dop_plans_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Взрослое направление", callback_data="1")],
        [InlineKeyboardButton(text="Детское направление", callback_data="2")],
        [InlineKeyboardButton(text="Курс обучения моделей PLUS SIZE", callback_data="3")],
        [InlineKeyboardButton(text="Киноактерская группа", callback_data="4")],
        [InlineKeyboardButton(text="Агентский взнос", callback_data="5")],
        [InlineKeyboardButton(text="Назад", callback_data="nazad")],
    ]
)


select_plans_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать еще один план обучения", callback_data="dop_plan")],
        [InlineKeyboardButton(text="Завершить оплату и регистрацию", callback_data="quit")],
    ]
)

pay_menu_ikbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Да", callback_data="yes")],
    ]
)
