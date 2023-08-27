from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from Settings.settings import settings

kbd_subcribing = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Канал',
            url=settings.data.channel_url
        ),
        InlineKeyboardButton(
            text='Чат',
            url=settings.data.group_url
        )
    ],
    [
        InlineKeyboardButton(
            text='Готово',
            callback_data='done'
        )
    ]
])

kbd_confirm_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data='allright'
        )
    ]
])

kbd_shop_cart = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Доставка',
            callback_data='delivery'
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data='delete'
        )
    ]
])

kbd_check_delivery = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text='Изменить данные',
            callback_data='delivery_change'
        )
    ],
    [
        InlineKeyboardButton(
            text='Оплата Юкасса',
            callback_data='pay_ukassa'
        )
    ]
])
