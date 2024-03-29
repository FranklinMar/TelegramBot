import re
from aiogram import types
from dispatcher import dp, bot

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton

from files.bot import kb
from dispatcher import factory as factory


@dp.message_handler(lambda message: message.text == "Замовлення💵")
async def process_order(message: types.Message):
    await message.answer("Виберіть, які товари ви хочете переглянути: ", reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'Не оплачені',
                                                            callback_data=f'not_paid')).add(
                                       InlineKeyboardButton(f'Оплачені',
                                                            callback_data=f'paid')))
    await message.answer("Для повернення в головне меню настисніть кнопку ⬇️", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("🔙 Повернутись в головне меню")) )


@dp.callback_query_handler(text="not_paid")
async def show_orders(call: CallbackQuery):
    orders = factory.get_ordering(call.from_user.id, False)
    price = 0
    if not orders:
        await call.message.answer("⚙️⚙️⚙️⚠️ Тут немає нічого... ⚠️ ⚙️⚙️⚙️", reply_markup=kb)
    else:
        for order in orders:
            full_products = factory.get_full_product(order[1])
            price += full_products[0][8]*order[4]
            await bot.send_photo(call.from_user.id, photo=full_products[0][10])
            await bot.send_message(call.from_user.id,
                                   f'{full_products[0][6]}\nОпис: {full_products[0][7]}\nЦіна: {full_products[0][8] } \nКолір: {full_products[0][3]} \nРозмір: {full_products[0][2]} \nКількість: {order[4]}',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'Видалити з замовлення ❌',
                                                            callback_data=f'Del {order[0]}')))
        await call.message.answer(f"Загальна сума замовлення становить: {price}💸\nДля оплати натисніть кнопку⬇️", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Перейти до оплати💶")).add(KeyboardButton("◀️Назад")))


@dp.callback_query_handler(lambda c: re.match('Del [0-9]+', c.data))
async def process_deleting(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ids = int(callback_query.data.split()[1])
    if ids:
        factory.connector.execute(f"DELETE FROM Ordering WHERE id = {ids};")
        factory.connector.commit()
        await callback_query.message.answer(text=f'✅ Продукт видалено ✅')
        await show_orders(callback_query)
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Продукту немає в замовленні. ❌")
