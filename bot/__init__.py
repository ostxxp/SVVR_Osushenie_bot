from aiogram import Bot, Dispatcher

from os import getenv
from dotenv import load_dotenv

load_dotenv('../.env')

bot = Bot(token=getenv("BOT_TOKEN"))
dp = Dispatcher()
