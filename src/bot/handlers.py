from bot import notifies
from bot.main import dp
from aiogram import types, F
from bot.keyboards import (
    main_menu_ikbd,
    main_menu_kbd,
    servise_menu_ikbd,
    get_plans_menu_ikbd,
    get_dop_plans_menu_ikbd,
    select_plans_menu_ikbd,
    choice_menu_ikbd,
)

from aiogram.enums import ContentType
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from bot.states import UserForm

from database.crud import CRUDUser, CRUDProgram, CRUDUserProgram

from config import APP_CONF


@dp.message(Command("start"))
async def start_cmd_message(message: types.Message, state: FSMContext):
    name = message.from_user.full_name
    await message.answer(f"Приветствуем в боте, {name}!", reply_markup=main_menu_ikbd)
    await state.clear()


@dp.callback_query(F.data == "rega")
async def main_menu_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите полное имя:")
    await callback.answer()
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


# @dp.message(Command("plans"))
# async def servise_menu_msg_handler(message: types.Message, state: FSMContext):
#     await message.answer("Выберите:", reply_markup=get_plans_menu_ikbd())
#     await state.set_state(UserForm.choice)  # Временный хэнд


@dp.callback_query(F.data == "plan")
async def servise_menu_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите:", reply_markup=get_plans_menu_ikbd())
    await callback.answer()


@dp.callback_query(F.data == "dop_plan")
async def dop_plan_menu_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer("Выберите:", reply_markup=get_dop_plans_menu_ikbd())
    await callback.answer()
    await callback.message.delete()


@dp.message(F.text == "Выбрать дополнительные планы обучения")
async def dop_plan_menu_msg_handler(message: types.Message, state: FSMContext):
    await message.answer("Выберите:", reply_markup=get_dop_plans_menu_ikbd())
    await message.delete()


@dp.callback_query(F.data == "nazad")
async def otmena_dop_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Выберите:")
    await callback.message.edit_reply_markup(reply_markup=select_plans_menu_ikbd)
    await state.clear()


@dp.callback_query(F.data == "1")
@dp.callback_query(F.data == "2")
@dp.callback_query(F.data == "3")
@dp.callback_query(F.data == "4")
@dp.callback_query(F.data == "5")
async def choice_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    program = CRUDProgram.get_program(int(callback.data))
    await state.update_data(num=callback.data)
    if program.has_subscription:
        await callback.message.edit_text("Выберите:")
        await callback.message.edit_reply_markup(reply_markup=choice_menu_ikbd)
    else:
        await num_all_pay_cb_handler(callback=callback, state=state)


# 1111 1111 1111 1026, 12/22, CVC 000
@dp.callback_query(F.data == "month")
async def num_pay_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    type_program = CRUDProgram.get_program(num=data["num"])
    type_program_num = str(type_program.num)
    await callback.message.delete()
    await callback.message.answer_invoice(
        title=type_program.title,
        description=type_program.description,
        provider_token=APP_CONF.PAYMENTS_TOKEN,
        currency="rub",
        is_flexible=False,
        prices=[types.LabeledPrice(label="Оплатить", amount=type_program.price)],
        payload=f"{type_program_num};true",
    )

    await state.clear()


@dp.callback_query(F.data == "all_pay")
async def num_all_pay_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    type_program = CRUDProgram.get_program(num=data["num"])
    type_program_num = str(type_program.num)
    await callback.message.answer_invoice(
        title=type_program.title,
        description=type_program.description,
        provider_token=APP_CONF.PAYMENTS_TOKEN,
        currency="rub",
        is_flexible=False,
        prices=[
            types.LabeledPrice(label="Оплатить", amount=type_program.price * type_program.month)
        ],
        payload=f"{type_program_num};false",
    )

    await state.clear()


@dp.pre_checkout_query()
async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@dp.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment_handler(message: types.Message):
    data = message.successful_payment.invoice_payload.split(";")
    program_num = int(data[0])
    is_sub = data[1] == "true"
    if CRUDUserProgram.check_and_minus_month(message.from_user.id, program_num):
        #  expire date что истекла уведомление о том что возобновлена
        await message.answer("Оплата прошла успешно!")
        if CRUDUserProgram.check_date:
            await notifies.send_to_sveta(
                text=(
                    f"{CRUDUser.get_name(message.from_user.id)} - подписка возобновлена - "
                    f"{CRUDProgram.get_program(program_num).title}"
                ),
            )
    else:
        CRUDUserProgram.add_prog(message.from_user.id, program_num, is_sub)
        await message.answer(
            "Оплата прошла успешно!",
            reply_markup=select_plans_menu_ikbd,
        )
        if is_sub:
            await notifies.send_to_sveta(
                text=(
                    f"{CRUDUser.get_name(message.from_user.id)} - оформлена подписка - "
                    f"{CRUDProgram.get_program(program_num).title}"
                ),
            )
        else:
            await notifies.send_to_sveta(
                text=(
                    f"{CRUDUser.get_name(message.from_user.id)} - оплачен весь курс - "
                    f"{CRUDProgram.get_program(program_num).title}"
                ),
            )


@dp.callback_query(F.data == "quit")
async def quit_cb_handler(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(
        "Желаем удачного обучения, ждем Вас на занятиях!", reply_markup=main_menu_kbd
    )
    await callback.message.delete()
    await state.clear()


# @dp.message()
# async def debug_msg(message: types.Message):
#     print(message.content_type)
