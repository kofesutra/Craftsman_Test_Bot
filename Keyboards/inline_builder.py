from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_inline_categories_kbd(list_kbd, list_of_codes, num_of_page, count_of_pages):

    inline_keyboard = None

    if num_of_page == 1:
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='⏹',
                    callback_data='none'
                ),
                InlineKeyboardButton(
                    text=f'{num_of_page} / {count_of_pages}',
                    callback_data='_'
                ),
                InlineKeyboardButton(
                    text='▶️',
                    callback_data='next'
                )
            ],
            [
                InlineKeyboardButton(
                    text=list_kbd[0],
                    callback_data=list_of_codes[0]
                )
            ],
            [
                InlineKeyboardButton(
                    text=list_kbd[1],
                    callback_data=list_of_codes[1]
                )
            ]
        ])

    elif num_of_page != 1 and num_of_page != count_of_pages:
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='◀️',
                    callback_data='previous'
                ),
                InlineKeyboardButton(
                    text=f'{num_of_page} / {count_of_pages}',
                    callback_data='_'
                ),
                InlineKeyboardButton(
                    text='▶️',
                    callback_data='next'
                )
            ],
            [
                InlineKeyboardButton(
                    text=list_kbd[0],
                    callback_data=list_of_codes[0]
                )
            ],
            [
                InlineKeyboardButton(
                    text=list_kbd[1],
                    callback_data=list_of_codes[1]
                )
            ]
        ])
    elif num_of_page != 1 and num_of_page == count_of_pages:
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='◀️',
                    callback_data='previous'
                ),
                InlineKeyboardButton(
                    text=f'{num_of_page} / {count_of_pages}',
                    callback_data='_'
                ),
                InlineKeyboardButton(
                    text='⏹',
                    callback_data='none'
                )
            ],
            [
                InlineKeyboardButton(
                    text=list_kbd[0],
                    callback_data=list_of_codes[0]
                )
            ],
            [
                InlineKeyboardButton(
                    text=list_kbd[1],
                    callback_data=list_of_codes[1]
                )
            ]
        ])

    return inline_keyboard


def create_inline_goods_kbd(list_of_codes, num_of_page, count_of_pages):

    inline_keyboard = None

    if num_of_page == 1:
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='⏹',
                    callback_data='none'
                ),
                InlineKeyboardButton(
                    text=f'{num_of_page} / {count_of_pages}',
                    callback_data='_'
                ),
                InlineKeyboardButton(
                    text='▶️',
                    callback_data='next'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Добавить в корзину',
                    callback_data=list_of_codes
                )
            ]
        ])

    elif num_of_page != 1 and num_of_page != count_of_pages:
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='◀️',
                    callback_data='previous'
                ),
                InlineKeyboardButton(
                    text=f'{num_of_page} / {count_of_pages}',
                    callback_data='_'
                ),
                InlineKeyboardButton(
                    text='▶️',
                    callback_data='next'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Добавить в корзину',
                    callback_data=list_of_codes
                )
            ]
        ])
    elif num_of_page != 1 and num_of_page == count_of_pages:
        inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(
                    text='◀️',
                    callback_data='previous'
                ),
                InlineKeyboardButton(
                    text=f'{num_of_page} / {count_of_pages}',
                    callback_data='_'
                ),
                InlineKeyboardButton(
                    text='⏹',
                    callback_data='none'
                )
            ],
            [
                InlineKeyboardButton(
                    text='Добавить в корзину',
                    callback_data=list_of_codes
                )
            ]
        ])

    return inline_keyboard
