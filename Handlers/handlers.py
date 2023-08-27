from aiogram.enums import ContentType
from aiogram.filters import Command, Text
from aiogram import F

from Handlers.Catalog.catalog import start_catalog, select_category, select_subcategory, select_goods, select_count, \
    confirm_choice, choice_confirmed
from Handlers.Faq.Inline_Mode.inline_mode import process_query
from Handlers.Faq.faq import start_faq
from Handlers.Start.start import on_start, subscribing
from Handlers.Shop_cart.pay import run_order, successful_payment, pre_checkout_query
from Handlers.Shop_cart.shop_cart import start_shop_cart, process_shop_cart, get_name, get_phone, get_address, check_delivery
from States.state_machine import States
from Utils.start_stop import start_bot, stop_bot
from Utils.loader import dp


def reg_handlers():
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    dp.message.register(on_start, Command(commands=['start']))
    dp.message.register(start_catalog, Text(text='Каталог'))
    dp.message.register(start_shop_cart, Text(text='Корзина'))
    dp.message.register(start_faq, Text(text='FAQ'))

    dp.inline_query.register(process_query)

    dp.callback_query.register(subscribing, States.subscribing, F.data == 'done')
    dp.callback_query.register(select_category, States.categories)
    dp.callback_query.register(select_subcategory, States.subcategories)
    dp.callback_query.register(select_goods, States.goods)
    dp.message.register(select_count, States.select_count)
    dp.message.register(confirm_choice, States.confirm_choice)
    dp.callback_query.register(choice_confirmed, States.choice_confirmed, F.data == 'allright')

    dp.message.register(start_shop_cart, States.shop_cart)
    dp.callback_query.register(process_shop_cart, States.process_shop_cart, F.data.in_(['delete', 'delivery']))
    dp.message.register(get_name, States.get_name)
    dp.message.register(get_phone, States.get_phone)
    dp.message.register(get_address, States.get_address)
    dp.callback_query.register(check_delivery, States.check_delivery,
                               F.data.in_(['delivery_change', 'pay_ukassa', 'pay_tinkoff']))

    dp.callback_query.register(run_order, States.run_order)
    dp.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)
    dp.pre_checkout_query.register(pre_checkout_query)
