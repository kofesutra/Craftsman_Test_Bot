from aiogram import Bot
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, FSInputFile

from DB.db_requests import Request
from Keyboards.inline import kbd_confirm_choice
from Keyboards.inline_builder import create_inline_categories_kbd, create_inline_goods_kbd
from Keyboards.reply import kbd_main
from Settings.settings import settings
from States.state_machine import States
from Utils.cbqa import cbqa


async def start_catalog(message: Message, state: FSMContext, bot: Bot, request: Request):
    button_count = 2  # Количество кнопок категорий отображаемых под сообщением

    await state.update_data(button_count=button_count)
    categories = await request.get_all(settings.db.categories)
    await state.update_data(categories=categories)
    count_of_categories = len(categories)
    index_of_category = 0
    await state.update_data(index_of_category=index_of_category)
    list_to_keyboard = [categories[index_of_category][2], categories[index_of_category+1][2]]
    list_of_codes = [categories[index_of_category][1], categories[index_of_category+1][1]]
    number_of_page = 1
    await state.update_data(number_of_page=number_of_page)
    count_of_pages = int(count_of_categories / 2)
    await state.update_data(count_of_pages=count_of_pages)

    # Создаём клавиатуру с нужными кнопками
    keyboard = create_inline_categories_kbd(list_to_keyboard, list_of_codes, number_of_page, count_of_pages)

    data = await message.answer('Это каталог товаров. Выбери категорию', reply_markup=keyboard)
    post_id = data.message_id
    await state.update_data(post_id=post_id)

    await state.set_state(States.categories)


async def select_category(call: CallbackQuery, state: FSMContext, bot: Bot, request: Request):
    button = call.data
    message = call.message
    await bot.answer_callback_query(callback_query_id=call.id)

    data = await state.get_data()
    categories = data['categories']
    index_of_category = data['index_of_category']
    post_id = data['post_id']
    user_id = data['user_id']
    count_of_pages = data['count_of_pages']
    button_count = data['button_count']

    if button == 'next':
        index_of_category = index_of_category + button_count
        await state.update_data(index_of_category=index_of_category)
        number_of_page = data['number_of_page'] + 1
        await state.update_data(number_of_page=number_of_page)
        list_to_keyboard = [categories[index_of_category][2], categories[index_of_category + 1][2]]
        list_of_codes = [categories[index_of_category][1], categories[index_of_category + 1][1]]

        await bot.delete_message(user_id, post_id)

        keyboard = create_inline_categories_kbd(list_to_keyboard, list_of_codes, number_of_page, count_of_pages)
        data = await message.answer('Это каталог товаров. Выбери категорию', reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

    elif button == 'previous':
        index_of_category = index_of_category - button_count
        await state.update_data(index_of_category=index_of_category)
        number_of_page = data['number_of_page'] - 1
        await state.update_data(number_of_page=number_of_page)
        list_to_keyboard = [categories[index_of_category][2], categories[index_of_category + 1][2]]
        list_of_codes = [categories[index_of_category][1], categories[index_of_category + 1][1]]

        await bot.delete_message(user_id, post_id)

        keyboard = create_inline_categories_kbd(list_to_keyboard, list_of_codes, number_of_page, count_of_pages)
        data = await message.answer('Это каталог товаров. Выбери категорию', reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

    elif button != 'none' and button != '_':

        # Далее переходим к подкатегории
        selected_category = int(button)
        await state.update_data(selected_category=selected_category)

        await bot.delete_message(user_id, post_id)

        button_count = 2
        await state.update_data(button_count=button_count)
        categories = await request.get_all(settings.db.subcategories)
        await state.update_data(categories=categories)
        count_of_categories = len(categories)
        index_of_category = 0
        await state.update_data(index_of_category=index_of_category)
        list_to_keyboard = [categories[index_of_category][2], categories[index_of_category + 1][2]]
        number_of_page = 1
        await state.update_data(number_of_page=number_of_page)
        count_of_pages = int(count_of_categories / 2)
        await state.update_data(count_of_pages=count_of_pages)

        keyboard = create_inline_categories_kbd(list_to_keyboard, list_to_keyboard, number_of_page, count_of_pages)
        data = await message.answer('Выбери размер', reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

        await state.set_state(States.subcategories)


async def select_subcategory(call: CallbackQuery, state: FSMContext, bot: Bot, request: Request):
    button = call.data
    message = call.message
    query = call.id
    await bot.answer_callback_query(callback_query_id=query)

    data = await state.get_data()
    categories = data['categories']
    selected_category = data['selected_category']
    index_of_category = data['index_of_category']
    post_id = data['post_id']
    user_id = data['user_id']
    count_of_pages = data['count_of_pages']
    button_count = data['button_count']

    if button == 'next':
        index_of_category = index_of_category + button_count
        await state.update_data(index_of_category=index_of_category)
        number_of_page = data['number_of_page'] + 1
        await state.update_data(number_of_page=number_of_page)
        list_to_keyboard = [categories[index_of_category][2], categories[index_of_category + 1][2]]

        await bot.delete_message(user_id, post_id)

        keyboard = create_inline_categories_kbd(list_to_keyboard, list_to_keyboard, number_of_page, count_of_pages)
        data = await message.answer('Выбери размер', reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

    elif button == 'previous':
        index_of_category = index_of_category - button_count
        await state.update_data(index_of_category=index_of_category)
        number_of_page = data['number_of_page'] - 1
        await state.update_data(number_of_page=number_of_page)
        list_to_keyboard = [categories[index_of_category][2], categories[index_of_category + 1][2]]

        await bot.delete_message(user_id, post_id)

        keyboard = create_inline_categories_kbd(list_to_keyboard, list_to_keyboard, number_of_page, count_of_pages)
        data = await message.answer('Выбери размер', reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

    elif button != 'none' and button != '_':
        selected_subcategory = button
        await state.update_data(selected_subcategory=selected_subcategory)
        await bot.delete_message(user_id, post_id)

        # TODO Заглушка: так как товаров в таблице только на три первые категории,
        #  то в оставшихся категориях дублируем первые три
        if selected_category == 4:
            selected_category = 1
        elif selected_category == 5:
            selected_category = 2
        elif selected_category == 6:
            selected_category = 3

        goods = await request.get_selected(settings.db.goods, 'category', selected_category)
        await state.update_data(goods=goods)
        count_of_goods = len(goods)
        index_of_goods = 0
        await state.update_data(index_of_goods=index_of_goods)
        goods_to_keyboard = goods[index_of_goods][2]
        picture_of_goods = goods[index_of_goods][3]
        price_of_goods = goods[index_of_goods][5]
        await state.update_data(price_of_goods=price_of_goods)
        number_of_page = 1
        await state.update_data(number_of_page=number_of_page)
        count_of_pages = count_of_goods
        await state.update_data(count_of_pages=count_of_pages)

        keyboard = create_inline_goods_kbd(goods_to_keyboard, number_of_page, count_of_pages)
        data = await message.answer_photo(FSInputFile(f"Media/{picture_of_goods}"),
                                          f'Товар: {goods_to_keyboard}\n\nЦена: {price_of_goods}', reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

        await state.set_state(States.goods)


async def select_goods(call: CallbackQuery, state: FSMContext, bot: Bot, request: Request):
    button = call.data
    message = call.message
    query = call.id
    await bot.answer_callback_query(callback_query_id=query)

    data = await state.get_data()
    goods = data['goods']
    index_of_goods = data['index_of_goods']
    post_id = data['post_id']
    user_id = data['user_id']
    count_of_pages = data['count_of_pages']
    price_of_goods = data['price_of_goods']

    if button == 'next':
        index_of_goods = index_of_goods + 1
        await state.update_data(index_of_goods=index_of_goods)
        number_of_page = data['number_of_page'] + 1
        await state.update_data(number_of_page=number_of_page)
        goods_to_keyboard = goods[index_of_goods][2]
        picture_of_goods = goods[index_of_goods][3]
        price_of_goods = goods[index_of_goods][5]

        await bot.delete_message(user_id, post_id)

        keyboard = create_inline_goods_kbd(goods_to_keyboard, number_of_page, count_of_pages)
        data = await message.answer_photo(FSInputFile(f"Media/{picture_of_goods}"),
                                          f'Товар: {goods_to_keyboard}\n\nЦена: {price_of_goods}',
                                          reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

    elif button == 'previous':
        index_of_goods = index_of_goods - 1
        await state.update_data(index_of_goods=index_of_goods)
        number_of_page = data['number_of_page'] - 1
        await state.update_data(number_of_page=number_of_page)
        goods_to_keyboard = goods[index_of_goods][2]
        picture_of_goods = goods[index_of_goods][3]
        price_of_goods = goods[index_of_goods][5]

        await bot.delete_message(user_id, post_id)

        keyboard = create_inline_goods_kbd(goods_to_keyboard, number_of_page, count_of_pages)
        data = await message.answer_photo(FSInputFile(f"Media/{picture_of_goods}"),
                                          f'Товар: {goods_to_keyboard}\n\nЦена: {price_of_goods}',
                                          reply_markup=keyboard)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

    elif button != 'none' and button != '_':
        selected_good = button
        await state.update_data(selected_good=selected_good)
        await state.update_data(selected_price=price_of_goods)

        await bot.delete_message(user_id, post_id)
        data = await message.answer('Укажи количество', reply_markup=None)
        post_id = data.message_id
        await state.update_data(post_id=post_id)

        await state.set_state(States.select_count)


async def select_count(message: Message, state: FSMContext, bot: Bot):
    selected_count = message.text
    await state.update_data(selected_count=selected_count)
    await state.set_state(States.confirm_choice)
    await confirm_choice(message, state, bot)


async def confirm_choice(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()
    post_id = data['post_id']
    user_id = data['user_id']
    selected_subcategory = data['selected_subcategory']
    selected_good = data['selected_good']
    selected_count = data['selected_count']
    selected_price = data['selected_price']
    total_price = selected_price * int(selected_count)
    await state.update_data(total_price=total_price)

    await bot.delete_message(user_id, post_id)

    data = await message.answer(f'Проверь, всё ли верно:\n\nВыбранный товар: {selected_good}\nРазмер: {selected_subcategory}\n'
                                f'Количество: {selected_count}\nЦена: {selected_price}\nСумма заказа: {total_price}',
                                reply_markup=kbd_confirm_choice)
    post_id = data.message_id
    await state.update_data(post_id=post_id)
    await state.set_state(States.choice_confirmed)


async def choice_confirmed(call: CallbackQuery, state: FSMContext, bot: Bot, request: Request):
    await cbqa(call, bot)
    message = call.message
    data = await state.get_data()

    id_in_table = await request.get_one('id', settings.db.users, 'user_id', f"{data['user_id']}")

    if id_in_table is not None:
        id_in_table = id_in_table[0]
        values = f"user_id='{data['user_id']}', username='{data['username']}', goods='{data['selected_good']}', size='{data['selected_subcategory']}', quantity='{data['selected_count']}', order_amount='{data['total_price']}'"
        await request.update_line(settings.db.users, values, 'id', f'{id_in_table}')
    else:
        columns = f'user_id, username, goods, size, quantity, order_amount'
        values = f"'{data['user_id']}', '{data['username']}', '{data['selected_good']}', " \
                 f"'{data['selected_subcategory']}', '{data['selected_count']}', '{data['total_price']}'"
        await request.add_line(settings.db.users, columns, values)

    await message.answer('Хорошо! Для оформления заказа нажми кнопку "Корзина"', reply_markup=kbd_main)

