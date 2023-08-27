from aiogram import Bot

from Settings.settings import settings


async def start_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bot.admin_id, text='Бот запущен')


async def stop_bot(bot: Bot):
    await bot.send_message(chat_id=settings.bot.admin_id, text='Бот остановлен')
