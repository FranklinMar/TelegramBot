from aiogram import types
from aiogram.types import CallbackQuery
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from dispatcher import dp, bot
from files.ordering import process_order
from dispatcher import factory as factory


@dp.callback_query_handler(text="paid")
async def show_paid_orders(call: CallbackQuery):
    orders = factory.get_ordering(call.from_user.id, True)
    if not orders:
        await call.message.answer("⚙️⚙️⚙️⚠️ Тут нічого немає... ⚠️ ⚙️⚙️⚙️")
    else:
        for order in orders:
            full_products = factory.get_full_product(order[1])
            product = factory.select_by_id_db(full_products[0][1])
            await bot.send_photo(call.from_user.id, photo=product[5])
            await bot.send_message(call.from_user.id, f'{product[1]}\nОпис: {product[2]}\nЦіну: {product[3]*order[4]} \nКолір: {full_products[0][3]} \nРозмір: {full_products[0][2]} \nКількість: {order[4]}', reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("◀️Назад")))


@dp.message_handler(text="◀️Назад")
async def cancels(message: types.Message):
    await process_order(message)
