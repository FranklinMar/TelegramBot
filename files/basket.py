import datetime
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from files.bot import process_start_command
from dispatcher import dp, bot
from aiogram.dispatcher import FSMContext
from Factory import Factory
from aiogram.dispatcher.filters.state import StatesGroup, State
from DatabaseFunctions import select_by_id_db
import re

factory = Factory("database.db")


class AmountRegister(StatesGroup):
    amount = State()


@dp.message_handler(state=AmountRegister.amount)
async def amount_input(message: types.Message, state: FSMContext):
    if message.text == "Cancel" or message.text == "Back":
        await state.finish()
        await show_basket(message)
        return
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer(
            "❌ Error! The amount was entered incorrectly ❌\n⚠️To exit, enter 'Cancel', 'Back' or '0' ")
        return
    if amount < 0:
        await message.answer("❌ Error! The amount cannot be negative ❌")
        return
    if amount == 0:
        await state.finish()
        await show_basket(message)
        return
    async with state.proxy() as data:
        idFull = data['idFull']
    if amount > factory.cursor.execute(f"SELECT count FROM FullProduct WHERE idFull = {idFull};").fetchone()[0]:
        await message.answer("❌ Error! The amount is bigger than storage capacity ❌")
        return
    sql = "INSERT INTO Ordering (idFull, idProfile, pay, count, date) VALUES (?, ?, ?, ?, ?);"
    factory.connector.execute(sql, (idFull, message.from_user.id, False, amount, datetime.date.today()))
    factory.connector.commit()
    factory.connector.execute(f"UPDATE FullProduct SET count = count - {amount} WHERE idFull = {idFull};")
    factory.connector.commit()
    await state.finish()
    await message.answer(text=f'✅ Product successfully added to your order. ✅',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'⬇️ Back',
                                        callback_data='basket')))


@dp.message_handler(lambda message: message.text == "Корзина👜")
async def show_basket(message):
    basket = [select_by_id_db(i[0]) for i in factory.cursor.execute(f"SELECT idProduct FROM Basket WHERE idProfile = "
                                                         f"{message.from_user.id};")]
    if len(basket) == 0:
        await message.answer("⚙️⚙️⚙️⚠️ It is so empty here... ⚠️ ⚙️⚙️⚙️")
    else:
        for i in basket:
            await bot.send_photo(message.from_user.id, photo=i[5])
            await bot.send_message(message.from_user.id, f'{i[1]}\nDescription: {i[2]}\nPrice: {i[3]}',
                                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
                                callback_data=f'Add {i[0]}')).add(InlineKeyboardButton(f'Remove from basket ❌',
                                callback_data=f'Delete {i[0]}')))
        await bot.send_message(message.from_user.id, "Choose action", reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton(f'⬇️ Back', callback_data=f'startMenu')))


@dp.callback_query_handler(lambda c: re.match('Add [0-9]+', c.data))
async def process_color(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup()
    factory.cursor.execute(f"SELECT color FROM FullProduct WHERE idProduct = {callback_query.data.split()[1]} AND "
                f"count > 0 GROUP BY color;")
    temp = factory.cursor.fetchall()
    if temp:
        for i in temp:
            keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'Size {callback_query.data.split()[1]}'
                                                                            f' {i[0]}'))
        keyboard.add(InlineKeyboardButton(text=f'⬇️ Back', callback_data='basket'))
        await bot.send_message(callback_query.from_user.id, '🟨🟥 Select color of the product 🟩🟦',
                               reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Sorry, the storage is out of this product. 🚫\n'
                                                            '⚠️Try again next time.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'⬇️ Back',
                                                                                            callback_data='basket')))


@dp.callback_query_handler(lambda c: re.match('Size [0-9]+ [A-Za-z]+', c.data))
async def process_size(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = InlineKeyboardMarkup()
    factory.cursor.execute(f"SELECT idFull, size FROM FullProduct WHERE idProduct = {callback_query.data.split()[1]} "
                           f"AND count > 0 AND color = '{callback_query.data.split()[2]}';")
    temp = factory.cursor.fetchall()
    if temp:
        for i in temp:
            keyboard.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'Count '
                                        f'{callback_query.data.split()[1]} {callback_query.data.split()[2]} {i[0]}'))
        keyboard.add(InlineKeyboardButton(text=f'⬇️ Back', callback_data='basket'))
        await bot.send_message(callback_query.from_user.id, '👕👖🧥 Select size of the product 👞👟🧤',
                               reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Sorry, the storage is out of this product. 🚫\n'
                                                            '⚠️Try again next time.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'⬇️ Back',
                                                                                            callback_data='basket')))


@dp.callback_query_handler(lambda c: re.match('Count [0-9]+ [A-Za-z]+ [0-9]+', c.data))
async def process_count(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    factory.cursor.execute(f"SELECT count FROM FullProduct WHERE idFull = {callback_query.data.split()[3]};")
    instance = factory.cursor.fetchone()
    if instance[0] > 0:
        await bot.send_message(callback_query.from_user.id, f"ℹ️ No. of products available : {instance[0]}\n\n"
                                                            f"✔️ Enter the amount of products to order 🔢")
        async with state.proxy() as data:
            data['idFull'] = callback_query.data.split()[3]

        await AmountRegister.amount.set()
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Sorry, the storage is out of this product. 🚫\n'
                                                            '⚠️Try again next time.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'⬇️ Back',
                                                                                            callback_data='basket')))


@dp.callback_query_handler(lambda c: re.match('Delete [0-9]+', c.data))
async def process_deleting(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ids = int(callback_query.data.split()[1])
    factory.cursor.execute(f"SELECT idBasket, idProduct FROM Basket WHERE idProfile = {callback_query.from_user.id} "
                f"AND idProduct = {ids};")
    ids = factory.cursor.fetchone()[0]
    if ids:
        factory.connector.execute(f"DELETE FROM Basket WHERE idBasket = {ids};")
        factory.connector.commit()
        await bot.send_message(callback_query.from_user.id, '✅ Product successfully removed from your basket. ✅',
                            reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'⬇️ Back',
                            callback_data='basket')))
        await show_basket(callback_query.message)
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌",
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text=f'⬇️ Back',
                                                                                            callback_data='basket')))


@dp.callback_query_handler(lambda c: "startMenu" == c.data)
async def process_redirect(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await process_start_command(callback_query.message)


@dp.callback_query_handler(lambda c: "basket" == c.data)
async def process_redirect(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await show_basket(callback_query)
