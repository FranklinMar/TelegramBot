from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq

import phonenumbers

from dispatcher import dp


class UserRegister(StatesGroup):
    waiting_for_surname = State()
    waiting_for_name = State()
    waiting_for_patronymic = State()
    waiting_for_birthday = State()
    waiting_for_phone_number = State()


@dp.message_handler(commands=['reg'])
async def register_start(message: types.Message):
    await message.answer("Введіть прізвище:",
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("Скасувати ❌")))
    await UserRegister.waiting_for_surname.set()


@dp.message_handler(state=UserRegister.waiting_for_surname)
async def surname_input(message: types.Message, state: FSMContext):

    await state.update_data(surname=message.text)
    await message.answer("Введіть ім'я:")
    await UserRegister.waiting_for_name.set()


@dp.message_handler(state=UserRegister.waiting_for_name)
async def name_input(message: types.Message, state: FSMContext):

    await state.update_data(name=message.text)
    await message.answer("Введіть по батькові:")
    await UserRegister.waiting_for_patronymic.set()


@dp.message_handler(state=UserRegister.waiting_for_patronymic)
async def patronymic_input(message: types.Message, state: FSMContext):

    await state.update_data(patronymic=message.text)
    await message.answer("Введіть дату народження:")
    await UserRegister.waiting_for_birthday.set()


@dp.message_handler(state=UserRegister.waiting_for_birthday)
async def birthday_input(message: types.Message, state: FSMContext):

    await state.update_data(birthday=message.text)
    await message.answer("Введіть номер телефону:")
    await UserRegister.waiting_for_phone_number.set()


@dp.message_handler(state=UserRegister.waiting_for_phone_number)
async def passport_number_input(message: types.Message, state: FSMContext):

    try:
        phone_number = phonenumbers.parse(message.text)
    except phonenumbers.NumberParseException:
        await message.answer(
            "Введений рядок не відповідає номеру телефона 😔\n"
            "Спробуйте ще раз")
        return

    if not phonenumbers.is_possible_number(phone_number):
        await message.answer("Некоректний номер телефону 😔\nСпробуйте ще раз")
        return

    await state.update_data(phone_number=message.text)
    user_data = await state.get_data()
    await message.answer("Реєстрація виконана успішно ✅")
    await state.finish()