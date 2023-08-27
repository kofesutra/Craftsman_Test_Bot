from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from DB.csv_export import csv_payment_success
from DB.db_success_payment import db_payment_success
from DB.xls_export import xls_payment_success
from DB.db_requests import Request
from States.state_machine import States
from Handlers.Shop_cart.pay import run_order
from Keyboards.inline import kbd_shop_cart, kbd_check_delivery
from Keyboards.reply import kbd_main
from Settings.settings import settings
from Utils.cbqa import cbqa


async def start_shop_cart(message: Message, state: FSMContext, bot: Bot, request: Request):
    user_id = message.from_user.id

    request = await request.get_selected(settings.db.users, 'user_id', user_id)
    if len(request) != 0:
        id_in_base = request[0][0]
        await state.update_data(id_in_base=id_in_base)
        username = request[0][2]
        goods = request[0][3]
        size = request[0][4]
        quantity = request[0][5]
        total_price = request[0][7]
        await state.update_data(goods=goods)
        await state.update_data(size=size)
        await state.update_data(quantity=quantity)
        await state.update_data(total_price=total_price)

        data = await message.answer(f'{username}, содержимое твоей корзины:\n\nТовар: {goods}\nРазмер: {size}\n'
                             f'Количество: {quantity}\n\nОбщая сумма: {total_price}', reply_markup=kbd_shop_cart)
        post_id = data.message_id
        await state.update_data(post_id=post_id)
    else:
        await message.answer('Твоя корзина пуста', reply_markup=kbd_main)

    await state.set_state(States.process_shop_cart)


async def process_shop_cart(call: CallbackQuery, state: FSMContext, bot: Bot, request: Request):
    await cbqa(call, bot)
    button = call.data
    message = call.message
    data = await state.get_data()
    id_in_base = data['id_in_base']
    if button == 'delete':
        post_id = data['post_id']
        user_id = data['user_id']
        await bot.delete_message(user_id, post_id)
        await request.delete_from_db(settings.db.users, 'id', id_in_base)
        await message.answer('Твоя корзина пуста')
    elif button == 'delivery':
        await message.answer('Для доставки товара мне нужны твои данные\n\nОтправь мне имя и фамилию')
        await state.set_state(States.get_name)


async def get_name(message: Message, state: FSMContext, bot: Bot):
    data = message.text
    await state.update_data(fullname=data)
    await message.answer('Отправь мне номер телефона')
    await state.set_state(States.get_phone)


async def get_phone(message: Message, state: FSMContext, bot: Bot):
    data = message.text
    await state.update_data(phone=data)
    await message.answer('Отправь мне адрес доставки')
    await state.set_state(States.get_address)


async def get_address(message: Message, state: FSMContext, bot: Bot):
    mess = message.text
    await state.update_data(address=mess)
    data = await state.get_data()
    fullname = data['fullname']
    phone = data['phone']
    address = data['address']
    await message.answer(f'Давай проверим введённые данные:\n\nИмя: {fullname}\nТелефон: {phone}\nАдрес: {address}',
                         reply_markup=kbd_check_delivery)
    await state.set_state(States.check_delivery)


async def check_delivery(call: CallbackQuery, state: FSMContext, bot: Bot, request: Request):
    button = call.data
    message = call.message
    user_id = call.from_user.id

    if button == 'delivery_change':
        await message.answer('Отправь мне имя и фамилию')
        await state.set_state(States.get_name)

    elif button == 'pay_ukassa':
        data = await state.get_data()
        values = f"fullname='{data['fullname']}', phone='{data['phone']}', address='{data['address']}'"
        await request.update_line(settings.db.users, values, 'user_id', user_id)

        # Оплата через Юкасса
        #await run_order(call, state, bot)

        await message.answer('Оплата прошла успешно\n\n'
                             'Выполненный заказ внесён в базу и в файлы xlsx и csv в папке Logs', reply_markup=kbd_main)

        await db_payment_success(state, request)
        await csv_payment_success(state)
        await xls_payment_success(state)
