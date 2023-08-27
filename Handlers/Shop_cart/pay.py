from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import PreCheckoutQuery, Message, CallbackQuery, LabeledPrice

from DB.csv_export import csv_payment_success
from DB.db_success_payment import db_payment_success
from DB.xls_export import xls_payment_success
from DB.db_requests import Request
from Keyboards.reply import kbd_main
from Settings.settings import settings


async def run_order(call: CallbackQuery, state: FSMContext, bot: Bot):
    message = call.message

    data = await state.get_data()
    label = f"Товар: {data['goods']}\nРазмер: {data['size']}\nКоличество: {data['quantity']}"
    amount = (data['total_price'])*100

    await bot.send_invoice(
        chat_id=message.chat.id,
        title='Тестовая покупка',
        description='В рамках тестового задания',
        payload='Bot pay',
        provider_token=settings.pay.pay_token,
        currency='rub',
        prices=[
            LabeledPrice(
                label=label,
                amount=amount
            )
        ],
        request_timeout=15
    )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


async def successful_payment(message: Message, state: FSMContext, request: Request):
    msg = f'Благодарим за покупку!\n\n' \
          f'{message.successful_payment.total_amount // 100} ' \
          f'{message.successful_payment.currency}\n\n' \
          f'Выполненный заказ внесён в базу и в файлы xlsx и csv в папке Logs'
    await message.answer(msg, reply_markup=kbd_main)

    await db_payment_success(state, request)  # Запиcь в БД
    await csv_payment_success(state)  # Запись в CSV
    await xls_payment_success(state)  # Запись в XLS



