from aiogram import Bot, Dispatcher

from Settings.settings import settings

bot = Bot(token=settings.bot.bot_token)
dp = Dispatcher()
