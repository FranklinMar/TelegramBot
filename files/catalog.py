from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq

from DatabaseFunctions import select_by_id_db
from dispatcher import dp, bot
from files.bot import kb


@dp.message_handler(lambda message: message.text == "Каталог🛍")
async def send_catalog(message: types.Message):
    kt = ReplyKeyboardMarkup()
    kt.add(KeyboardButton("Жіночий одяг"))
    kt.add(KeyboardButton('Чоловічий одяг'))
    kt.add(KeyboardButton("Повернутись у меню"))
    await message.answer('Виберіть для кого цей товар', reply_markup=kt)


@dp.message_handler(text="Жіночий одяг")
async def send_woman(message: types.Message):
    woman = InlineKeyboardMarkup()
    woman.add(InlineKeyboardButton(text="Верхній одяг", callback_data="Outerwear_woman"))
    woman.add(InlineKeyboardButton(text="Толстовки", callback_data="Hoodies_woman"))
    woman.add(InlineKeyboardButton(text="Аксесуари", callback_data="Accessories_woman"))
    woman.add(InlineKeyboardButton(text="Штани", callback_data="Pants_woman"))
    woman.add(InlineKeyboardButton(text="Білизна", callback_data="Underwear_woman"))
    await message.answer("Оберіть:", reply_markup=woman)


@dp.message_handler(text="Повернутись у меню")
async def send_back(message: types.Message):
    await message.answer("Оберіть дію:", reply_markup=kb)


@dp.message_handler(text="Чоловічий одяг")
async def send_man(message: types.Message):
    man = InlineKeyboardMarkup()
    man.add(InlineKeyboardButton(text="Верхній одяг", callback_data="Outerwear_man"))
    man.add(InlineKeyboardButton(text="Толстовки", callback_data="Hoodies_man"))
    man.add(InlineKeyboardButton(text="Аксесуари", callback_data="Accessories_man"))
    man.add(InlineKeyboardButton(text="Штани", callback_data="Pants_man"))
    man.add(InlineKeyboardButton(text="Білизна", callback_data="Underwear_man"))
    await message.answer("Оберіть:", reply_markup=man)


@dp.callback_query_handler(text="Accessories_man")
async def send_accessories(call: CallbackQuery):
    await call.message.answer("Accessories_man")
    await sql_read(call, 'Accessories_man')


@dp.callback_query_handler(text="Accessories_woman")
async def send_accessories(call: CallbackQuery):
    await call.message.answer("Accessories_woman")
    await sql_read(call, 'Accessories_woman')


@dp.callback_query_handler(text="Outerwear_man")
async def send_outerwear(call: CallbackQuery):
    await call.message.answer("Outerwear_man")
    await sql_read(call, 'Outerwear_man')


@dp.callback_query_handler(text="Outerwear_woman")
async def send_outerwear(call: CallbackQuery):
    await call.message.answer("Outerwear_woman")
    await sql_read(call, 'Outerwear_woman')


@dp.callback_query_handler(text="Hoodies_man")
async def send_hoodies(call: CallbackQuery):
    await call.message.answer("Hoodies_man")
    await sql_read(call, 'Hoodies_man')


@dp.callback_query_handler(text="Hoodies_woman")
async def send_hoodies(call: CallbackQuery):
    # await call.message.answer("Hoodies_woman")
    await sql_read(call, 'Hoodies_woman')


@dp.callback_query_handler(text="Accessories_woman")
async def send_accessories(call: CallbackQuery):
    await call.message.answer("Accessories_woman")
    await sql_read(call, 'Accessories_woman')


@dp.callback_query_handler(text="Pants_man")
async def send_pants(call: CallbackQuery):
    await call.message.answer("Pants_man")
    await sql_read(call, 'Pants_man')


@dp.callback_query_handler(text="Pants_woman")
async def send_pants(call: CallbackQuery):
    await call.message.answer("Pants_woman")
    await sql_read(call, 'Pants_woman')


@dp.callback_query_handler(text="Underwear_man")
async def send_underwear(call: CallbackQuery):
    await call.message.answer("Underwear_man")
    await sql_read(call, 'Underwear_man')


@dp.callback_query_handler(text="Underwear_woman")
async def send_underwear(call: CallbackQuery):
    await call.message.answer("Underwear_woman")
    await sql_read(call, 'Underwear_woman')


def sql_start():
    global base, cur
    base = sq.connect('database.db')
    cur = base.cursor()
    if base:
        print('Database connected.')


def get_name_product_by_id(id_product):
    result = cur.execute("SELECT * FROM Product WHERE idProduct = ?", (id_product,)).fetchone()
    return result[1]


async def sql_add_command(id_element, id_user):
    print(id_user)
    id_elements = cur.execute("SELECT * FROM Basket WHERE idProfile = ? AND idProduct = ?", (id_user, id_element)).fetchone()
    if id_elements is None:
        cur.execute('INSERT INTO Basket (idProfile, idProduct) VALUES (?,?);', (id_user, id_element))
        base.commit()
        return True
    else:
        return False


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('add '))
async def add_callback_run(callback_query: types.CallbackQuery):
    if await sql_add_command(callback_query.data.replace('add ', ''), callback_query.from_user.id):
        await callback_query.answer(text=f"{get_name_product_by_id(callback_query.data.replace('add ', ''))} added.",
                                    show_alert=True)
    else:
        await callback_query.answer(
            text=f"{get_name_product_by_id(callback_query.data.replace('add ', ''))} is already "
                 f"in your basket.", show_alert=True)


async def sql_read(message, type_clothes):
    sql_start()
    # for ret in cur.execute("SELECT * FROM Product WHERE type = :typeCl", {"typeCl": type_clothes}).fetchall():
    #     await bot.send_photo(message.from_user.id, photo=open('1.jpg', 'rb'))
    #     await bot.send_message(message.from_user.id, f'{ret[1]}\nDescription: {ret[2]}\nPrice: {ret[3]}')
    #     await bot.send_message(message.from_user.id, text='^', reply_markup=InlineKeyboardMarkup(). \
    #                            add(InlineKeyboardButton(f'Add to order {ret[1]}', callback_data=f'add {ret[0]}')))
    products = [select_by_id_db(i[0]) for i in
                cur.execute("SELECT * FROM Product WHERE type = :typeCl", {"typeCl": type_clothes}).fetchall()]
    if not len(products):
        await message.answer("Empty category...")
    else:
        for product in products:
            await bot.send_photo(message.from_user.id, photo=product[5])
            await bot.send_message(message.from_user.id, f'{product[1]}\nDescription: {product[2]}\nPrice: {product[3]}'
                                   , reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton(f'Add to order {product[1]}',
                                                            callback_data=f'add {product[0]}')))
