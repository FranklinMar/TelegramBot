from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq

from Factory import Factory
from dispatcher import dp, bot

kb = ReplyKeyboardMarkup()
kb.add(KeyboardButton('Реєcтpація'))
kb.add(KeyboardButton('Каталог'))
kb.add(KeyboardButton('Корзина'))
kb.add(KeyboardButton('Інформація'))
kb.add(KeyboardButton('Допомога'))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    factory = Factory("database.db")
    if factory.cursor.execute(f"SELECT * FROM Profile WHERE id = {message.from_user.id};").fetchall():
        pass
    else:
        sql = "INSERT INTO Profile (id) VALUES (?);"
        factory.cursor.execute(sql, (message.from_user.id,))
        factory.connector.commit()
    await message.reply(f"Привет!\nID:{message.from_user.id}\n{message}", reply_markup=kb)


@dp.message_handler(lambda message: message.text == "Корзина")
async def process_start_command(message: types.Message):
    kt = ReplyKeyboardMarkup()
    kt.add(KeyboardButton('Переглянути товари в корзині'))
    kt.add(KeyboardButton('Видалити товар'))
    kt.add(KeyboardButton('Оплатити товари'))
    kt.add(KeyboardButton('Повернутись у меню'))
    await message.reply('Оберіть дію', reply_markup=kt)


@dp.message_handler(lambda message: message.text == "Переглянути товари в корзині")
async def add(message: types.Message):
    await message.answer('Товари')


@dp.message_handler(lambda message: message.text == "Видалити товар")
async def dell(message: types.Message):
    await message.answer("Видалення товарів")


@dp.message_handler(lambda message: message.text == "Оплатити товари")
async def pay(message: types.Message):
    await message.answer("Оплата")


@dp.message_handler(lambda message: message.text == "Інформація")
async def inform(message: types.Message):
    kt = ReplyKeyboardMarkup()
    kt.add(KeyboardButton('Написати відгук'))
    kt.add(KeyboardButton('Переглянути відгуки'))
    kt.add(KeyboardButton('Переглянути інформацію про магазин'))
    kt.add(KeyboardButton('Повернутись у меню'))
    await message.reply('Оберіть вид інформації', reply_markup=kt)


@dp.message_handler(lambda message: message.text == "Написати відгук")
async def write_review(message: types.Message):
    await message.answer("Написання відгуку")


@dp.message_handler(lambda message: message.text == "Переглянути відгуки")
async def look_reviews(message: types.Message):
    await message.answer("Переглядання відгуків")


@dp.message_handler(lambda message: message.text == "Переглянути інформацію про відгуки")
async def look_inform(message: types.Message):
    await message.answer("Інформація про магазин")


# @dp.message_handler()
# async def echo(message: types.Message):
#     await message.answer(message.text, reply_markup=kb)

