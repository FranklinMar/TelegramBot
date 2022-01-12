import datetime

from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove, ReplyKeyboardMarkup, \
    KeyboardButton, CallbackQuery
# import sqlite3 as sq
from files.bot import process_start_command, kb as kb
from dispatcher import dp, bot
from aiogram.dispatcher import FSMContext
from dispatcher import factory as factory
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
# from files.bot import kb
from DatabaseFunctions import select_by_id_db
import re

# factory = Factory("database.db")


class AmountRegister(StatesGroup):
    amount = State()


# def sql_start():
#     global base, cur
#     base = sq.connect('database.db')
#     if base:
#         print('Database connected.')
#         cur = base.cursor()


@dp.message_handler(state=AmountRegister.amount)
async def amount_input(message: types.Message, state: FSMContext):
    if message.text == "Вийти" or message.text == "Назад":
        await state.finish()
        await show_basket(message)
        return
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer(
            "❌ Помилка! Введена неправильна кількість товарів ❌\n⚠️Щоб повернутися, введіть 'Вийти', 'Назад' або '0' ")
        return
    if amount < 0:
        await message.answer("❌ Помилка! Кількість не може бути від'ємною ❌")
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
    await message.answer(text=f'✅ Товар успішно додано до вашого замовлення. ✅',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Back',
                                                                                        callback_data='basket')))  # ,
                         # show_alert=True)
    # await show_basket(message)


@dp.message_handler(lambda message: message.text == "Корзина👜")
async def show_basket(message):
    # ids = message.from_user.id
    # show(message)
    # sql_start()
    # sql = f"SELECT idProduct FROM Basket WHERE idProfile = {message.from_user.id}"

    basket = [select_by_id_db(i[0]) for i in factory.cursor.execute(f"SELECT idProduct FROM Basket WHERE idProfile = "
                                                         f"{message.from_user.id};")]
    if len(basket) == 0:
        await bot.send_message(message.from_user.id, "️⚠️ Тут так пусто... ⚠️ ", reply_markup=
        ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("🔙 Повернутись в головне меню")))
        # InlineKeyboardMarkup().add(InlineKeyboardButton('⬇️ Назад', callback_data=f'startMenu')))
    else:
        await bot.send_message(message.from_user.id, "---Ваша Корзина---", reply_markup=
        ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("🔙 Повернутись в головне меню")))
        for i in basket:
            await bot.send_photo(message.from_user.id, photo=i[5])
            await bot.send_message(message.from_user.id, f'{i[1]}\nОпис: {i[2]}\nЦіна: {i[3]}',
                                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Додати для покупки ⏩🟢',
                                callback_data=f'Add {i[0]}')).add(InlineKeyboardButton(f'Видалити з корзини ❌',
                                callback_data=f'Delete {i[0]}')))
        # await bot.send_message(message.from_user.id, "Choose action", reply_markup=ReplyKeyboardRemove())
        # await bot.send_message(message.from_user.id, "Оберіть дію", reply_markup=InlineKeyboardMarkup()
        #                        .add(InlineKeyboardButton('⬇️ Назад', callback_data=f'startMenu')))


@dp.callback_query_handler(lambda c: re.match('Add [0-9]+', c.data))
async def process_color(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # print(f"Gotcha Color Select. {callback_query.data}")
    # ids = int(callback_query.data.split()[1])
    # cur.execute(f"SELECT idBasket, idProduct FROM Basket WHERE idProfile = {callback_query.from_user.id} "
    #             f"AND idProduct = {ids};")
    # ids = cur.fetchone()
    # if cur.fetchone()[0]:
    # if ids:
    keyboard = InlineKeyboardMarkup()
    factory.cursor.execute(f"SELECT color FROM FullProduct WHERE idProduct = {callback_query.data.split()[1]} AND "
                f"count > 0 GROUP BY color;")
    temp = factory.cursor.fetchall()
    if temp:
        for i in temp:
            keyboard.add(InlineKeyboardButton(text=f'{i[0]}', callback_data=f'Size {callback_query.data.split()[1]}'
                                                                            f' {i[0]}'))
        keyboard.add(InlineKeyboardButton(text='⬇️ Назад', callback_data='basket'))
        # base.execute(f"")
        # pass
        # reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
        #             callback_data=f'/AddOrder {i[0]}')).add(InlineKeyboardButton(f'Add to buying ⏩🟢',
        #                          callback_data=f'/Delete {i[0]}')))
        await bot.send_message(callback_query.from_user.id, '🟨🟥 Оберіть колір товару 🟩🟦',
                               reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Вибачте, цей товар вичерпано зі складу. 🚫\n'
                                                            '⚠️Спробуйте пізніше.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))

    # else:
    #     await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")
        # await message.answer("❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: re.match('Size [0-9]+ [A-Za-z]+', c.data))
async def process_size(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    # ids = int(callback_query.data.split()[1])
    # print("Gotcha Size select.")
    # cur.execute(f"SELECT idBasket, idProduct FROM Basket WHERE idProfile = {callback_query.from_user.id} "
    #            f"AND idProduct = {ids};")
    # ids = cur.fetchone()
    # if cur.fetchone()[0]:
    # if ids:
    keyboard = InlineKeyboardMarkup()
    factory.cursor.execute(f"SELECT idFull, size FROM FullProduct WHERE idProduct = {callback_query.data.split()[1]} "
                           f"AND count > 0 AND color = '{callback_query.data.split()[2]}';")
    temp = factory.cursor.fetchall()
    if temp:
        for i in temp:
            keyboard.add(InlineKeyboardButton(text=f'{i[1]}', callback_data=f'Count '
                                        f'{callback_query.data.split()[1]} {callback_query.data.split()[2]} {i[0]}'))
        keyboard.add(InlineKeyboardButton(text='⬇️ Назад', callback_data='basket'))
        # base.execute(f"")
        # pass
        # reply_markup = InlineKeyboardMarkup().add(InlineKeyboardButton(f'Add to buying ⏩🟢',
        #             callback_data=f'/AddOrder {i[0]}')).add(InlineKeyboardButton(f'Add to buying ⏩🟢',
        #                          callback_data=f'/Delete {i[0]}')))
        factory.cursor.execute(f"SELECT * FROM Product WHERE idProduct = {callback_query.data.split()[1]};")
        temporary = factory.cursor.fetchone()
        if not temporary:
            await bot.send_message(callback_query.from_user.id, '🚫 Вибачте, цей товар не присутній у магазині. 🚫',
                                   reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))
            return
        if temporary[6] == "Accessories_woman" or temporary[6] == "Accessories_man":
            await bot.send_message(callback_query.from_user.id, '---🧥Розміри🧥---\nS - маленький\nM - середній\nL - '
                                                                'великий')
        elif temporary[4] == "Woman":
            await bot.send_photo(callback_query.from_user.id, photo=open("./photos/ dimenGridW.jpg", "rb"))
        else:
            await bot.send_photo(callback_query.from_user.id, photo=open("./photos/dimenGridM.jpg", "rb"))
        await bot.send_message(callback_query.from_user.id, '👕👖🧥 Оберіть розмір товару 👞👟🧤', reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Вибачте, цей товар вичерпано зі складу. 🚫\n'
                                                            '⚠️Спробуйте пізніше.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))
    # else:
    #     await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: re.match('Count [0-9]+ [A-Za-z]+ [0-9]+', c.data))
async def process_count(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    # print("Gotcha Count Select.")
    # ids = int(callback_query.data.split()[1])
    # cur.execute(f"SELECT idBasket FROM Basket WHERE idProfile = {callback_query.from_user.id} AND idProduct = {ids};")
    # ids = cur.fetchone()
    # if ids:
    factory.cursor.execute(f"SELECT count FROM FullProduct WHERE idFull = {callback_query.data.split()[3]};")
    instance = factory.cursor.fetchone()
    if instance[0] > 0:
        await bot.send_message(callback_query.from_user.id, f"ℹ️ Кількість доступних товарів : {instance[0]}\n\n"
                                                            f"✔️ Введіть кількість товарів для замовлення 🔢")
        async with state.proxy() as data:
            data['idFull'] = callback_query.data.split()[3]

        await AmountRegister.amount.set()
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Вибачте, цей товар вичерпано зі складу. 🚫\n'
                                                            '⚠️Спробуйте пізніше.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))
        # await show_basket(callback_query.message)
    # cur.execute(f"SELECT id, size FROM FullProduct WHERE idProduct = {ids[2]} AND size = "
    #             f"{callback_query.data.split()[2]};")
    # else:
    #     await bot.send_message(callback_query.from_user.id, "❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: re.match('Delete [0-9]+', c.data))
async def process_deleting(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    ids = int(callback_query.data.split()[1])
    factory.cursor.execute(f"SELECT idBasket, idProduct FROM Basket WHERE idProfile = {callback_query.from_user.id} "
                f"AND idProduct = {ids};")
    ids = factory.cursor.fetchone()
    if ids:
        factory.connector.execute(f"DELETE FROM Basket WHERE idBasket = {ids[0]};")
        factory.connector.commit()
        # await callback_query.answer(text=f'✅ Product successfully removed from your basket. ✅',
        #                             show_alert=True)
        await bot.send_message(callback_query.from_user.id, '✅ Товар успішно видалено з Вашої корзини. ✅',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))
        # await bot.send_message(callback_query.from_user.id, f'✅ Product successfully removed from your basket. ✅')
        # await show_basket(callback_query.message)
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Цього товару немає у вашій корзині. ❌",
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))
        # await show_basket(callback_query.message)
        # message.answer("❌ Product is not in your basket. ❌")


@dp.callback_query_handler(lambda c: "startMenu" == c.data)
async def process_redirect(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await process_start_command(callback_query.message)


@dp.callback_query_handler(lambda c: "basket" == c.data)
async def process_basket(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await show_basket(callback_query)
    # print("Showbasket called")

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
