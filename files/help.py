from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

from dispatcher import dp
from files.authorization import cancel


class Support(StatesGroup):
    problem = State()
    description = State()


@dp.message_handler(text='Допомога🆘')
async def register_start(message: types.Message):
    await message.answer("Привіт! Введи з чим пов'язана твоя проблема: ",
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("🔙 Повернутись в головне меню")))
    await Support.problem.set()


@dp.message_handler(state=Support.problem)
async def surname_input(message: types.Message, state: FSMContext):
    if message.text == "🔙 Повернутись в головне меню":
        await cancel(message, state)
        return
    await state.update_data(surname=message.text)
    await message.answer("Опиши проблему повністю:")
    await Support.description.set()


@dp.message_handler(state=Support.description)
async def name_input(message: types.Message, state: FSMContext):
    if message.text == "🔙 Повернутись в головне меню":
        await cancel(message, state)
        return
    await state.update_data(name=message.text)
    await message.answer("Введіть по батькові:")
    await UserRegister.patronymic.set()


@dp.message_handler(state=UserRegister.patronymic)
async def patron_input(message: types.Message, state: FSMContext):
    if message.text == "🔙 Повернутись в головне меню":
        await cancel(message, state)
        return
    await state.update_data(patronymic=message.text)
    await message.answer("Введіть номер телефону:")
    await UserRegister.phone_number.set()