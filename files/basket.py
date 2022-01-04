from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq
from dispatcher import dp, bot
# from files.bot import kb
from DatabaseFunctions import select_by_id_db
import re


def sql_start():
    global base, cur
    base = sq.connect('database.db')
    if base:
        print('Database connected.')
        cur = base.cursor()


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
                            callback_data=f'Add {i[0]}')).add(InlineKeyboardButton(f'Remove from basket ❌',
                            callback_data=f'Delete {i[0]}')))
        await bot.send_message(message.from_user.id, "Choose action", reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton(f'⬇️ Back', callback_data=f'startMenu')))


@dp.callback_query_handler(lambda c: re.match('Add [0-9]+', c.data))
async def process_ordering(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ids = int(callback_query.data.split()[1])
    cur.execute(f"SELECT idBasket FROM Basket WHERE idProfile = {callback_query.from_user.id} AND idProduct = {ids};")
    ids = cur.fetchone()[0]
    # if cur.fetchone()[0]:
    if ids:
        keyboard = InlineKeyboardMarkup()
        cur.execute(f"SELECT color FROM FullProduct WHERE idProduct = {ids};")
        for i in cur.fetchall():
            keyboard.add(InlineKeyboardButton(f'{i[0]}', callback_data=f'{callback_query.data} {i[0]}'))
        # base.execute(f"")
        # pass
        # reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
        #             callback_data=f'/AddOrder {i[0]}')).add(InlineKeyboardButton(f'Add to buying ⏩🟢',
        #                          callback_data=f'/Delete {i[0]}')))
        await bot.send_message(callback_query.from_user.id, f'🟨🟥 Select color of the product 🟩🟦', reply_markup=keyboard)

    else:
        await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")
        #await message.answer("❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: re.match('Delete [0-9]+', c.data))
async def process_deleting(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ids = int(callback_query.data.split()[1])
    cur.execute(f"SELECT idBasket FROM Basket WHERE idProfile = {callback_query.from_user.id} AND idProduct = {ids};")
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
