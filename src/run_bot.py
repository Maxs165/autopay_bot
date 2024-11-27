import asyncio
from bot.main import dp, bot
from aiogram.types import BotCommand
from bot import handlers

from database.utils import init_db

from scheduler import schedule_jobs


async def on_startup():
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить бота"),
        ]
    )
    await bot.set_my_description("ОПИСАНИЕ")
    init_db()


async def main():
    schedule_jobs()
    dp.startup.register(on_startup)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Остановлено вручную")
