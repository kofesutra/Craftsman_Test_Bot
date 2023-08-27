import openpyxl
from aiogram.fsm.context import FSMContext


async def xls_payment_success(state: FSMContext):
    xls_file = 'Logs/XLSX.xlsx'

    data = await state.get_data()
    values_csv = [data['user_id'], data['username'], data['goods'], data['size'], data['quantity'], data['total_price'],
                  data['fullname'], data['phone'], data['address']]

    book = openpyxl.load_workbook(xls_file)
    sheet = book.active
    sheet.append(values_csv)
    book.save(xls_file)
