from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):
    subscribing = State()

    # Каталог
    categories = State()
    subcategories = State()
    goods = State()
    select_count = State()
    confirm_choice = State()
    choice_confirmed = State()

    # Корзина покупок
    shop_cart = State()
    process_shop_cart = State()

    get_name = State()
    get_phone = State()
    get_address = State()
    check_delivery = State()

    run_order = State()

