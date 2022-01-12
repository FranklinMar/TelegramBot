import datetime
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from files.bot import process_start_command
from dispatcher import dp, bot
from aiogram.dispatcher import FSMContext
from dispatcher import factory as factory
from aiogram.dispatcher.filters.state import StatesGroup, State
from DatabaseFunctions import select_by_id_db
import re


class AmountRegister(StatesGroup):
    amount = State()


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
                                                                                        callback_data='basket')))


@dp.message_handler(lambda message: message.text == "Корзина👜")
async def show_basket(message):
    basket = [select_by_id_db(i[0]) for i in factory.cursor.execute(f"SELECT idProduct FROM Basket WHERE idProfile = "
                                                         f"{message.from_user.id};")]
    if len(basket) == 0:
        await bot.send_message(message.from_user.id, "️⚠️ Тут так пусто... ⚠️ ", reply_markup=
        InlineKeyboardMarkup().add(InlineKeyboardButton('⬇️ Назад', callback_data=f'startMenu')))
    else:
        await bot.send_message(message.from_user.id, "---Ваша Корзина---", reply_markup=ReplyKeyboardRemove())
        for i in basket:
            await bot.send_photo(message.from_user.id, photo=i[5])
            await bot.send_message(message.from_user.id, f'{i[1]}\nОпис: {i[2]}\nЦіна: {i[3]}',
                                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(f'Додати для покупки ⏩🟢',
                                callback_data=f'Add {i[0]}')).add(InlineKeyboardButton(f'Видалити з корзини ❌',
                                callback_data=f'Delete {i[0]}')))
        await bot.send_message(message.from_user.id, "Оберіть дію", reply_markup=InlineKeyboardMarkup()
                               .add(InlineKeyboardButton('⬇️ Назад', callback_data=f'startMenu')))


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
        keyboard.add(InlineKeyboardButton(text='⬇️ Назад', callback_data='basket'))
        await bot.send_message(callback_query.from_user.id, '🟨🟥 Оберіть колір товару 🟩🟦',
                               reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Вибачте, цей товар вичерпано зі складу. 🚫\n'
                                                            '⚠️Спробуйте пізніше.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
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
        keyboard.add(InlineKeyboardButton(text='⬇️ Назад', callback_data='basket'))
        await bot.send_message(callback_query.from_user.id, '👕👖🧥 Оберіть розмір товару 👞👟🧤',
                               reply_markup=keyboard)
    else:
        await bot.send_message(callback_query.from_user.id, '🚫 Вибачте, цей товар вичерпано зі складу. 🚫\n'
                                                            '⚠️Спробуйте пізніше.',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))


@dp.callback_query_handler(lambda c: re.match('Count [0-9]+ [A-Za-z]+ [0-9]+', c.data))
async def process_count(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
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
        await bot.send_message(callback_query.from_user.id, '✅ Товар успішно видалено з Вашої корзини. ✅',
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))
    else:
        await bot.send_message(callback_query.from_user.id, "❌ Цього товару немає у вашій корзині. ❌",
                               reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='⬇️ Назад',
                                                                                            callback_data='basket')))


@dp.callback_query_handler(lambda c: "startMenu" == c.data)
async def process_redirect(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await process_start_command(callback_query.message)


@dp.callback_query_handler(lambda c: "basket" == c.data)
async def process_basket(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    await show_basket(callback_query)
