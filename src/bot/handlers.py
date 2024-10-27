from bot.main import dp
from aiogram import types, F
from bot.keyboards import (
    main_menu_ikbd,
    servise_menu_ikbd,
    plans_menu_ikbd,
    dop_plans_menu_ikbd,
    select_plans_menu_ikbd,
    # choice_menu_ikbd,
)

# from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ContentType
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from bot.states import UserForm

from database.crud import CRUDUser, CRUDProgram

from config import APP_CONF


@dp.message(Command("start"))
async def start_cmd_message(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    await message.answer(f"Приветствуем в боте, {name}", reply_markup=main_menu_ikbd)
    await state.clear()


@dp.callback_query(F.data == "rega")
async def main_menu_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите полное имя:")
    await state.set_state(UserForm.name)


@dp.message(UserForm.name)
async def name_handler(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите номер телефона:")
    await state.set_state(UserForm.number)


@dp.message(UserForm.number)
async def number_handler(message: types.Message, state: FSMContext):
    await state.update_data(number=message.text)
    data = await state.get_data()
    CRUDUser.create(
        tguid=message.from_user.id,
        name=data["name"],
        number=data["number"],
    )
    await message.answer("Пользователь успешно зарегистрирован!", reply_markup=servise_menu_ikbd)
    await state.clear()


#  сюда вогнать выбор действия
# @dp.callback_query(F.data == "")


@dp.message(Command("plans"))
async def servise_menu_msg_handler(message: types.Message, state: FSMContext):
    await message.answer("Выберите:", reply_markup=plans_menu_ikbd)
    await state.set_state(UserForm.num)  # Временный хэнд


@dp.callback_query(F.data == "plan")
async def servise_menu_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите:", reply_markup=plans_menu_ikbd)
    await state.set_state(UserForm.num)
    await callback.answer()


@dp.callback_query(F.data == "dop_plan")
async def dop_plan_menu_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите:", reply_markup=dop_plans_menu_ikbd)
    await state.set_state(UserForm.num)
    await callback.answer()
    await callback.message.delete()


@dp.callback_query(F.data == "nazad")
async def otmena_dop_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите:")
    await callback.message.edit_reply_markup(reply_markup=select_plans_menu_ikbd)
    await state.clear()


# @dp.callback_query(UserForm.num)
# async def choice_cb_handler(callback: types.CallbackQuery, state: FSMContext):
#     await callback.message.edit_text("Выберите:")
#     await callback.message.edit_reply_markup(reply_markup=choice_menu_ikbd)
#     await callback.message.delete()
# F.data == "month"


# 1111 1111 1111 1026, 12/22, CVC 000
@dp.callback_query(UserForm.num)
async def num_menu_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    type_program = CRUDProgram.get_program(callback.data)  # было (num = callback.data)
    type_program_num = str(type_program.num)
    await callback.message.answer_invoice(
        title=type_program.title,
        description=type_program.description,
        provider_token=APP_CONF.PAYMENTS_TOKEN,
        currency="rub",
        is_flexible=False,
        prices=[types.LabeledPrice(label="Оплатить", amount=type_program.price)],
        payload=type_program_num,
    )

    await state.clear()


@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment_handler(message: types.Message):
    CRUDUser.add_day(message.from_user.id, 30)
    CRUDUser.add_prog(message.from_user.id, message.successful_payment.invoice_payload)
    await message.answer(
        f"Оплата прошла успешно! {message.successful_payment.invoice_payload}.",
        reply_markup=select_plans_menu_ikbd,
    )


@dp.callback_query(F.data == "quit")
async def quit_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Желаем удачного обучения, ждем Вас на занятиях!")
    await callback.message.delete()


# @dp.callback_query(F.data == "yes")
# async def pay_cb_handler(callback: types.CallbackQuery, state: FSMContext):
#     CRUDUser.add_day(tguid=callback.from_user.id, day=int(30))
#     await callback.message.answer(
#         f"Оплачено, осталось {CRUDUser.get_day(tguid=callback.from_user.id)} дней"
#     )
#     await state.clear()


# # buy
# if PAYMENTS_TOKEN.split(":")[1] == "TEST":
#     await bot.send_message(message.chat.id, "Тестовый платеж!!!")

# await bot.send_invoice(
#     message.chat.id,
#     title="Подписка на бота",
#     description="Активация подписки на бота на 1 месяц",
#     provider_token=config.PAYMENTS_TOKEN,
#     currency="rub",
#     photo_url="https://www.aroged.com/wp-content/uploads/2022/06/Telegram-has-a-premium-subscription.jpg",
#     photo_width=416,
#     photo_height=234,
#     photo_size=416,
#     is_flexible=False,
#     prices=[PRICE],
#     start_parameter="one-month-subscription",
#     payload="test-invoice-payload",
# )


# @dp.message()
# async def debug_msg(message: types.Message):
#     print(message.content_type)
