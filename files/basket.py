from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq
from files.bot import process_start_command
from dispatcher import dp, bot
from aiogram.dispatcher import FSMContext
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
# from files.bot import kb
from DatabaseFunctions import select_by_id_db
import re


class AmountRegister(StatesGroup):
    amount = State()


def sql_start():
    global base, cur
    base = sq.connect('database.db')
    if base:
        print('Database connected.')
        cur = base.cursor()


@dp.message_handler(state=AmountRegister.amount)
async def amount_input(message: types.Message, state: FSMContext):
    if message.text == "Cancel" or message.text == "Back":
        await state.finish()
        await show_basket(message)
        return
    try:
        amount = int(message.text)
    except ValueError as e:
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
    if amount > cur.execute(f"SELECT count FROM FullProduct WHERE idFull = {idFull};").fetchone()[0]:
        await message.answer("❌ Error! The amount is bigger than storage capacity ❌")
        return
    sql = "INSERT INTO Ordering (idFull, idProfile, pay, count, date) VALUES (?, ?, ?, ?, ?);"
    base.execute(sql, (idFull, message.from_user.id, False, amount, None))
    base.commit()
    base.execute(f"UPDATE FullProduct SET count = count - {amount} WHERE idFull = {idFull};")
    base.commit()
    await state.finish()
    await message.answer(text=f'✅ Product successfully added to your order. ✅')  # ,
                         # show_alert=True)
    await show_basket(message)


@dp.message_handler(lambda message: message.text == "Корзина")
async def show_basket(message: types.Message):
    # ids = message.from_user.id
    # show(message)
    sql_start()
    # sql = f"SELECT idProduct FROM Basket WHERE idProfile = {message.from_user.id}"

    basket = [select_by_id_db(i[0]) for i in cur.execute(f"SELECT idProduct FROM Basket WHERE idProfile = "
                                                         f"{message.from_user.id};")]
    if len(basket) == 0:
        await message.answer("⚙️⚙️⚙️⚠️ It is so empty here... ⚠️ ⚙️⚙️⚙️")
    else:
        for i in basket:
            await bot.send_photo(message.from_user.id, photo=i[5])
            await bot.send_message(message.from_user.id, f'{i[1]}\nDescription: {i[2]}\nPrice: {i[3]}',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
                                                                                                callback_data=f'Add {i[0]}')).add(
                                       InlineKeyboardButton(f'Remove from basket ❌',
                                                            callback_data=f'Delete {i[0]}')))
        await bot.send_message(message.from_user.id, "Choose action", reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton(f'⬇️ Back', callback_data=f'startMenu')))


@dp.callback_query_handler(lambda c: re.match('Add [0-9]+', c.data))
async def process_color(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    print(f"Gotcha Color Select. {callback_query.data}")
    ids = int(callback_query.data.split()[1])
    cur.execute(f"SELECT idBasket, idProduct FROM Basket WHERE idProfile = {callback_query.from_user.id} "
                f"AND idProduct = {ids};")
    ids = cur.fetchone()
    # if cur.fetchone()[0]:
    if ids:
        keyboard = InlineKeyboardMarkup()
        cur.execute(f"SELECT color FROM FullProduct WHERE idProduct = {ids[1]} AND count > 0 GROUP BY color;")
        temp = cur.fetchall()
        if temp:
            for i in temp:
                keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'Size {callback_query.data.split()[1]}'
                                                                                f' {i[0]}'))
            # base.execute(f"")
            # pass
            # reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
            #             callback_data=f'/AddOrder {i[0]}')).add(InlineKeyboardButton(f'Add to buying ⏩🟢',
            #                          callback_data=f'/Delete {i[0]}')))
            await bot.send_message(callback_query.from_user.id, '🟨🟥 Select color of the product 🟩🟦',
                                   reply_markup=keyboard)
        else:
            await bot.send_message(callback_query.from_user.id, '🚫 Sorry, the storage is out of this product. 🚫\n'
                                                                '⚠️Try again next time.')

    else:
        await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")
        # await message.answer("❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: re.match('Size [0-9]+ [A-Za-z]+', c.data))
async def process_size(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ids = int(callback_query.data.split()[1])
    print("Gotcha Size select.")
    cur.execute(f"SELECT idBasket, idProduct FROM Basket WHERE idProfile = {callback_query.from_user.id} "
                f"AND idProduct = {ids};")
    ids = cur.fetchone()
    # if cur.fetchone()[0]:
    if ids:
        keyboard = InlineKeyboardMarkup()
        cur.execute(f"SELECT idFull, size FROM FullProduct WHERE idProduct = {ids[1]} AND count > 0 AND color = "
                    f"'{callback_query.data.split()[2]}';")
        temp = cur.fetchall()
        if temp:
            for i in temp:
                keyboard.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'Count '
                                                                                f'{callback_query.data.split()[1]} {callback_query.data.split()[2]} {i[0]}'))
            # base.execute(f"")
            # pass
            # reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
            #             callback_data=f'/AddOrder {i[0]}')).add(InlineKeyboardButton(f'Add to buying ⏩🟢',
            #                          callback_data=f'/Delete {i[0]}')))
            await bot.send_message(callback_query.from_user.id, '👕👖🧥 Select size of the product 👞👟🧤',
                                   reply_markup=keyboard)
        else:
            await bot.send_message(callback_query.from_user.id, '🚫 Sorry, the storage is out of this product. 🚫\n'
                                                                '⚠️Try again next time.')
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: re.match('Count [0-9]+ [A-Za-z]+ [0-9]+', c.data))
async def process_count(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    print("Gotcha Count Select.")
    ids = int(callback_query.data.split()[1])
    cur.execute(f"SELECT idBasket FROM Basket WHERE idProfile = {callback_query.from_user.id} AND idProduct = {ids};")
    ids = cur.fetchone()
    if ids:
        cur.execute(f"SELECT count FROM FullProduct WHERE idFull = {callback_query.data.split()[3]};")
        await bot.send_message(callback_query.from_user.id, f"ℹ️ No. of products available : {cur.fetchone()[0]}\n\n"
                                                            f"✔️ Enter the amount of products to order 🔢")
        async with state.proxy() as data:
            data['idFull'] = callback_query.data.split()[3]

        await AmountRegister.amount.set()
        # cur.execute(f"SELECT id, size FROM FullProduct WHERE idProduct = {ids[2]} AND size = "
        #             f"{callback_query.data.split()[2]};")
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: re.match('Delete [0-9]+', c.data))
async def process_deleting(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ids = int(callback_query.data.split()[1])
    cur.execute(f"SELECT idBasket, idProduct FROM Basket WHERE idProfile = {callback_query.from_user.id} "
                f"AND idProduct = {ids};")
    ids = cur.fetchone()[0]
    if ids:
        base.execute(f"DELETE FROM Basket WHERE idBasket = {ids};")
        base.commit()
        await callback_query.answer(text=f'✅ Product successfully removed from your basket. ✅',
                                    show_alert=True)
        # await bot.send_message(callback_query.from_user.id, f'✅ Product successfully removed from your basket. ✅')
        await show_basket(callback_query.message)
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")
        # message.answer("❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: "startMenu" == c.data)
async def process_redirect(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await process_start_command(callback_query.message)

# @dp.callback_query_handler(func=lambda c: c.data == 'button1')
# async def process_callback_button1(callback_query: types.CallbackQuery):
#     await bot.answer_callback_query(callback_query.id)
#     await bot.send_message(callback_query.from_user.id, 'Нажата первая кнопка!')


# async def show(message: types.Message):
#     sql_start()
#     # sql = f"SELECT idProduct FROM Basket WHERE idProfile = {message.from_user.id}"
#     basket = [select_by_id_db(i[0]) for i in cur.execute(f"SELECT idProduct FROM Basket WHERE idProfile = "
#                                                          f"{message.from_user.id};")]
#     if len(basket) == 0:
#         await message.answer("⚠️ It is so empty here... ⚠️ :gear:")
#     else:
#         for i in basket:
#             await bot.send_photo(message.from_user.id, photo=i[5])
#             await bot.send_message(message.from_user.id, f'{i[1]}\nDescription: {i[2]}\nPrice: {i[3]}',
#                     reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
#                             callback_data=f'/AddOrder {i[0]}')).add(InlineKeyboardButton(f'Add to buying ⏩🟢',
#                                     callback_data=f'/Delete {i[0]}')))
#         await bot.send_message(message.from_user.id, "\n", reply_markup=InlineKeyboardMarkup()
#                                .add(InlineKeyboardButton(f'⬇️ Back', callback_data=f'/start')))


# @dp.message_handler(commands="AddOrder")
# async def add_order(message: types.Message):
#     ids = int(message.text.split()[1])
#     cur.execute(f"SELECT idBasket FROM Basket WHERE idProfile = {message.from_user.id} AND idProduct = {ids};")
#     ids = cur.fetchone()[0]
#     # if cur.fetchone()[0]:
#     if ids:
#         keyboard = InlineKeyboardMarkup()
#         cur.execute(f"SELECT color FROM FullProduct WHERE idProduct = {ids};")
#         for i in cur.fetchall():
#             keyboard.add(InlineKeyboardButton(f'{i[0]}', callback_data=f'/AddOrder {message.text.split()[1]} {i[0]}'))
#         # base.execute(f"")
#         # pass
#         # reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
#         #             callback_data=f'/AddOrder {i[0]}')).add(InlineKeyboardButton(f'Add to buying ⏩🟢',
#         #                          callback_data=f'/Delete {i[0]}')))
#         await bot.send_message(message.from_user.id, f'🟨🟥 Select color of the product 🟩🟦', reply_markup=keyboard)
#
#     else:
#         await message.answer("❌ Product is not in your basket. ❌")


# @dp.message_handler(commands="Delete")
# async def delete_basket(message: types.Message):
#     ids = int(message.text.split()[1])
#     cur.execute(f"SELECT idBasket FROM Basket WHERE idProfile = {message.from_user.id} AND idProduct = {ids};")
#     ids = cur.fetchone()[0]
#     if ids:
#         base.execute(f"DELETE FROM Basket WHERE idBasket = {ids};")
#         await bot.send_message(message.from_user.id, f'✅ Product successfully removed from your basket. ✅')
#         await show_basket(message)
#     else:
#         await message.answer("❌ Product is not in your basket. ❌")
