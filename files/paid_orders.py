from aiogram import types
from aiogram.types import CallbackQuery

from dispatcher import dp, bot
from DatabaseFunctions import select_by_id_db
from Factory import Factory
factory = Factory("database.db")


@dp.callback_query_handler(text="paid")
async def show_paid_orders(call: CallbackQuery):
    orders = factory.get_ordering(call.from_user.id, True)
    if not orders:
        await call.message.answer("⚙️⚙️⚙️⚠️ Тут нічого немає... ⚠️ ⚙️⚙️⚙️")
    else:
        for order in orders:
            full_products = factory.get_full_product(order[1])
            product = select_by_id_db(full_products[0][1])
            await bot.send_photo(call.from_user.id, photo=product[5])
            await bot.send_message(call.from_user.id, f'{product[1]}\nОпис: {product[2]}\nЦіну: {product[3]*order[4]} Колір: {full_products[0][3]} Розмір: {full_products[0][2]} Кількість: {order[4]}')

