from _csv import writer

from aiogram.fsm.context import FSMContext


async def csv_payment_success(state: FSMContext):
    csv_file = 'Logs/CSV.csv'
    data = await state.get_data()
    values_csv = [data['user_id'], data['username'], data['goods'], data['size'], data['quantity'], data['total_price'],
                  data['fullname'], data['phone'], data['address']]

    with open(csv_file, mode='a', encoding='utf-8', newline='') as file:
        writer_object = writer(file, delimiter=',')
        writer_object.writerow(values_csv)
        file.close()
