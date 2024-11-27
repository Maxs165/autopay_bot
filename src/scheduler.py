from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler  # BackgroundScheduler
from database.crud import CRUDUserProgram, CRUDProgram, CRUDUser

from bot import notifies
from time import sleep


async def notify_users_subscription():
    users = CRUDUserProgram.get_all()
    for u in users:
        if u.is_sub and u.months_left > 0:
            delta = u.expire_date - date.today()
            day = delta.days
            if day == 2:
                await notifies.send_notify(
                    u.user_tguid, notifies.two_days_left_notify, num=u.program_num
                )
            if day == 1:
                await notifies.send_notify(
                    u.user_tguid, notifies.one_day_left_notify, num=u.program_num
                )
            if day == 0:
                await notifies.send_notify(u.user_tguid, notifies.expire_notify, num=u.program_num)
                await notifies.send_to_sveta(
                    text=(
                        f"{CRUDUser.get_name(u.user_tguid)} - просрочена оплата подписки на курс -"
                        f" {CRUDProgram.get_program(u.program_num).title}"
                    ),
                )
            sleep(0.1)


def schedule_jobs():
    scheduler.start()
    scheduler.add_job(notify_users_subscription, "cron", hour=2, minute=45)


scheduler = AsyncIOScheduler()  # BackgroundScheduler()
