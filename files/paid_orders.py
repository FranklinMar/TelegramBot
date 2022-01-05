from aiogram import types
from aiogram.types import CallbackQuery

from dispatcher import dp, bot
from DatabaseFunctions import select_by_id_db, select_by_id_db_full
from Factory import Factory
factory = Factory("database.db")


@dp.callback_query_handler(text="paid")
async def show_paid_orders(call: CallbackQuery):
    orders = factory.get_ordering(call.from_user.id, True)
    if len(orders) == 0:
        await call.message.answer("⚙️⚙️⚙️⚠️ It is so empty here... ⚠️ ⚙️⚙️⚙️")
    else:
        for order in orders:
            # sql = f"SELECT * FROM FullProduct WHERE idFull = {int(t[1])};"
            # k = factory.cursor.execute(sql).fetchall()
            full_products = factory.get_full_product(order[1])
            product = select_by_id_db(full_products[0][1])
            await bot.send_photo(call.from_user.id, photo=product[5])
            await bot.send_message(call.from_user.id, f'{product[1]}\nDescription: {product[2]}\nPrice: {product[3]*order[4]} Color: {full_products[0][3]} Size: {full_products[0][2]} Count: {order[4]}')

