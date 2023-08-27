from aiogram.fsm.context import FSMContext

from DB.db_requests import Request
from Settings.settings import settings


async def db_payment_success(state: FSMContext, request: Request):
    data = await state.get_data()
    columns = f'user_id, username, goods, size, quantity, order_amount, fullname, phone, address'
    values = f"'{data['user_id']}', '{data['username']}', '{data['goods']}', " \
             f"'{data['size']}', '{data['quantity']}', '{data['total_price']}', " \
             f"'{data['fullname']}', '{data['phone']}', '{data['address']}'"
    await request.add_line(settings.db.orders, columns, values)

    await request.delete_from_db(settings.db.users, 'user_id', f"{data['user_id']}")
