import logging
from datetime import datetime

from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from DB.db_requests import Request
from Settings.settings import settings
from States.state_machine import States
from Keyboards.inline import kbd_subcribing
from Keyboards.reply import kbd_main
from Utils.cbqa import cbqa
from Utils.check_subscribing import check_subscribing


async def on_start(message: Message, state: FSMContext, bot: Bot, request: Request):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    username = message.from_user.username
    await state.update_data(username=username)
    first_name_here = message.from_user.first_name
    await state.update_data(first_name=first_name_here)
    last_name_here = message.from_user.last_name
    await state.update_data(last_name=last_name_here)

    if await check_subscribing(user_id, bot):

        # TODO Далее в коде тестового задания не будет обработки ошибок, чтобы облегчить читаемость,
        #  но в "боевом" боте они должны быть
        data = None
        try:
            data = await message.answer(
                f'Привет, {username}!\nРад тебя видеть!\n\nНажми кнопку "Каталог" чтобы сделать покупку',
                reply_markup=kbd_main)
        except Exception as ex:
            logging.error(f'[ERROR]: {ex}', exc_info=True)

        # Запоминаем пост чтобы удалить его позже
        post_id = data.message_id
        await state.update_data(post_id=post_id)
    else:
        data = await message.answer(f'Привет, {username}!\n\n'
                                    f'Прежде, чем продолжишь, подпишись на канал и чат, а затем нажми кнопку "Готово"',
                                    reply_markup=kbd_subcribing)
        post_id = data.message_id
        await state.update_data(post_id=post_id)
        await state.set_state(States.subscribing)


async def subscribing(call: CallbackQuery, state: FSMContext, bot: Bot):
    button = call.data
    message = call.message
    if button == 'done':
        await cbqa(call, bot)
        data = await state.get_data()
        user_id = data['user_id']
        post_id = data['post_id']

        if await check_subscribing(user_id, bot):

            # Удаляем предыдущее сообщение
            await bot.delete_message(user_id, post_id)

            data = await message.answer(
                f'Хорошо, ты подписан на канал и чат.\n\nНажми кнопку "Каталог" чтобы сделать покупку',
                reply_markup=kbd_main)
            post_id = data.message_id
            await state.update_data(post_id=post_id)
        else:
            await bot.delete_message(user_id, post_id)
            data = await message.answer(
                f'Ты ещё не подписан на канал и чат\nПрежде, чем продолжишь, подпишись, а затем нажми кнопку "Готово"',
                reply_markup=kbd_subcribing)
            post_id = data.message_id
            await state.update_data(post_id=post_id)
