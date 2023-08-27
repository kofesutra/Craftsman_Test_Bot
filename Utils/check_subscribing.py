import logging

from aiogram import Bot

from Settings.settings import settings


async def check_subscribing(user_id: int, bot: Bot) -> bool:
    result_channel = None
    result_group = None

    try:
        result_channel = await bot.get_chat_member(settings.data.channel_to_check, user_id)
    except Exception as ex:
        logging.error(f'[ERROR]: {ex}', exc_info=True)

    try:
        result_group = await bot.get_chat_member(settings.data.group_to_check, user_id)
    except Exception as ex:
        logging.error(f'[ERROR]: {ex}', exc_info=True)

    if result_channel.status == 'left' or result_group.status == 'left':
        return False
    else:
        return True
