from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kbd_main = ReplyKeyboardMarkup(resize_keyboard=True,
                               keyboard=[
                                   [
                                       KeyboardButton(text='Каталог'),
                                       KeyboardButton(text='Корзина'),
                                       KeyboardButton(text='FAQ')
                                   ]
                               ]
                               )
