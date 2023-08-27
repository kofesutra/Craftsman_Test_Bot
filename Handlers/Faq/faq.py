from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


async def start_faq(message: Message, state: FSMContext, bot: Bot):
    await message.answer('Если хотите что-либо узнать, в поле "Написать сообщение" напишите @Craftsman_test_bot и начинайте вводить свой вопрос')