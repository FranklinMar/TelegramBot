from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import  ReplyKeyboardMarkup, KeyboardButton

from dispatcher import dp, factory
from files.authorization import cancel, my_profile, register_start

from files.bot import kb


class Support(StatesGroup):
    problem = State()
    description = State()


@dp.message_handler(text='Допомога🆘')
async def helps(message: types.Message):
    if my_profile(message.from_user.id):
        await message.answer("Привіт! Введи з чим пов'язана твоя проблема: ",
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).row(
                                 KeyboardButton("🔙 Повернутись в головне меню")))
        await Support.problem.set()
    else:
        await message.answer("У вас немає профілю зареєструйтесь будь ласка")
        await register_start(message, "help")


@dp.message_handler(state=Support.problem)
async def problem_input(message: types.Message, state: FSMContext):
    if message.text == "🔙 Повернутись в головне меню":
        await cancel(message, state)
        return
    await state.update_data(problem=message.text)
    await message.answer("Опиши проблему повністю:")
    await Support.description.set()


@dp.message_handler(state=Support.description)
async def description_input(message: types.Message, state: FSMContext):
    if message.text == "🔙 Повернутись в головне меню":
        await cancel(message, state)
        return
    await state.update_data(description=message.text)
    new_support = await state.get_data()
    sql = f"INSERT INTO Support (Problem, Description, idProfile) VALUES (?, ?, ?);"
    data = (new_support["problem"], new_support["description"], message.from_user.id)
    factory.cursor.execute(sql, data)
    factory.connector.commit()
    await message.answer("Дякуємо, після вирішення проблеми ми зателефонуємо вам✅", reply_markup=kb)
    await state.finish()


