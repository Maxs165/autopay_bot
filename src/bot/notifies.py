from bot.main import bot

two_days_left_notify = "У вас осталось два дня подписки"
one_day_left_notify = "У вас осталcя один день подписки"
expire_notify = "У вас закончилась подписка"


async def send_notify(tguid: int, text: str):
    await bot.send_message(tguid, text=text)
