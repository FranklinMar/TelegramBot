from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton


from Factory import Factory
from dispatcher import dp, bot
from DatabaseFunctions import insert_db

kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(KeyboardButton('Профіль🙎‍♂️🙍‍♀️'))
kb.add(KeyboardButton('Каталог🛍'))
kb.add(KeyboardButton('Корзина👜'))
kb.add(KeyboardButton('Замовлення💵'))
kb.add(KeyboardButton('Допомога🆘'))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    factory = Factory("database.db")
    if factory.cursor.execute(f"SELECT * FROM Profile WHERE id = {message.from_user.id};").fetchall():
        pass
    else:
        sql = "INSERT INTO Profile (id) VALUES (?);"
        factory.cursor.execute(sql, (message.from_user.id,))
        factory.connector.commit()
    await message.reply(f"Привет!", reply_markup=kb)



