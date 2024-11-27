from bot.main import bot

from database.crud import CRUDProgram
from aiogram import types

from config import APP_CONF

two_days_left_notify = "Через 2 дня истекает подписка на курс, продление 👇 "
one_day_left_notify = "Через 1 день истекает подписка на курс, продление 👇"
expire_notify = "У ваc истекла подписка на курс, продление 👇"


async def send_notify(tguid: int, text: str, num: int):
    await bot.send_message(tguid, text=text)
    type_program = CRUDProgram.get_program(num)
    type_program_num = str(type_program.num)
    await bot.send_invoice(
        tguid,
        title=type_program.title,
        description=type_program.description,
        provider_token=APP_CONF.PAYMENTS_TOKEN,
        currency="rub",
        is_flexible=False,
        prices=[types.LabeledPrice(label="Оплатить", amount=type_program.price)],
        payload=f"{type_program_num};true",
    )


async def send_to_sveta(text: str):
    await bot.send_message(547935847, text=text)
