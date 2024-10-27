from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from config import APP_CONF
from aiogram.enums import ParseMode

import logging


logging.basicConfig(level=logging.INFO)


bot = Bot(token=APP_CONF.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()
