from apscheduler.schedulers.background import BackgroundScheduler
from database.crud import CRUDUser

from bot import notifies
from time import sleep


def decrease_subscription_days_job():
    CRUDUser.all_minus_day()


def notify_users_subscription():
    users = CRUDUser.get_all()
    for u in users:
        if u.day == 2:
            notifies.send_notify(u.tguid, notifies.two_days_left_notify)
        if u.day == 1:
            notifies.send_notify(u.tguid, notifies.one_day_left_notify)
        if u.day == 0:
            notifies.send_notify(u.tguid, notifies.expire_notify)
        sleep(0.1)


def schedule_jobs():
    scheduler.start()
    scheduler.add_job(decrease_subscription_days_job, "cron", hour=0, minute=0)
    scheduler.add_job(notify_users_subscription, "cron", hour=15, minute=0)


scheduler = BackgroundScheduler()
