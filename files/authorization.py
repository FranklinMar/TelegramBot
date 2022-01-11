from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq

from Factory import Factory
from files.bot import kb
import phonenumbers

from dispatcher import dp

factory = Factory("database.db")


class UserRegister(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    phone_number = State()


class UserEdit(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    phone_number = State()


change = ReplyKeyboardMarkup(resize_keyboard=True)
change.row(KeyboardButton("Yes"), KeyboardButton("No"))


@dp.message_handler(commands=['reg'])
async def register_start(message: types.Message):
    await message.answer("Hello! Enter your surname:",
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("🔙Cancel")))
    await UserRegister.surname.set()


@dp.message_handler(state=UserRegister.surname)
async def surname_input(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await cancel(message, state)
        return
    await state.update_data(surname=message.text)
    await message.answer("Enter your name:")
    await UserRegister.name.set()


@dp.message_handler(state=UserRegister.name)
async def name_input(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await cancel(message, state)
        return
    await state.update_data(name=message.text)
    await message.answer("Enter your patronymic:")
    await UserRegister.patronymic.set()


@dp.message_handler(state=UserRegister.patronymic)
async def birthday_input(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await cancel(message, state)
        return
    await state.update_data(patronymic=message.text)
    await message.answer("Enter phone number:")
    await UserRegister.phone_number.set()


@dp.message_handler(state=UserRegister.phone_number)
async def passport_number_input(message: types.Message, state: FSMContext):
    if message.text == "Cancel":
        await cancel(message, state)
        return
    try:
        phone_number = phonenumbers.parse(message.text)
    except phonenumbers.NumberParseException:
        await message.answer(
            "Error! The phone number was entered incorrectly😔")
        return
    if not phonenumbers.is_possible_number(phone_number):
        await message.answer("Error! The phone number was entered incorrectly😔")
        return

    await state.update_data(phone_number=message.text)
    new_user = await state.get_data()

    sql = f"UPDATE Profile SET surname = ?, name = ?, patronymic = ?, phone_number = ? WHERE id = ?;"
    data = (new_user["surname"], new_user["name"], new_user["patronymic"], new_user["phone_number"], message.from_user.id)
    factory.cursor.execute(sql, data)
    factory.connector.commit()
    await message.answer("Registration completed ✅")
    await state.finish()
    await profile(message)


@dp.message_handler(Text(equals="🔙Cancel"))
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Cancel",
                         reply_markup=kb)


@dp.message_handler(lambda message: message.text == "Профіль🙎‍♂️🙍‍♀️")
async def profile(message: types.Message):
    if my_profile(message.from_user.id):
        await message.answer(my_profile(message.from_user.id), reply_markup=change)
    else:
        await message.answer("You do not have a profile, please register!")
        await register_start(message)


def my_profile(id):
    profiles = factory.cursor.execute(f"SELECT * FROM Profile WHERE id = {id};").fetchall()
    for profile in profiles:
        if profile[1]:
            return f"Your profile:\nName: {profile[1]}\nSurname: {profile[2]}\nPatronymic: {profile[3]}\nPhone_number: {profile[4]}\nWant to change your profile?"
        else:
            return None


@dp.message_handler(text="No")
async def no(message: types.Message):
    await message.answer("Choose an operation", reply_markup=kb)


@dp.message_handler(text="Yes")
async def yes(message: types.Message):
    edits = InlineKeyboardMarkup()
    edits.add(InlineKeyboardButton(text="Name", callback_data="edit_Name"))
    edits.add(InlineKeyboardButton(text="Surname", callback_data="edit_Surname"))
    edits.add(InlineKeyboardButton(text="Patronymic", callback_data="edit_Patronymic"))
    edits.add(InlineKeyboardButton(text="Phone number", callback_data="edit_Phonenumber"))
    await message.answer("Choose what you want to change:", reply_markup=edits)


@dp.callback_query_handler(lambda call: call.data.startswith('edit'))
async def callback_worker_promo(call: CallbackQuery):
    model_type, object = call.data.split("_")
    if object == "Name":
        await call.message.answer("Enter name:")
        await UserEdit.name.set()
    if object == "Surname":
        await call.message.answer("Enter surname:")
        await UserEdit.surname.set()
    if object == "Patronymic":
        await call.message.answer("Enter patronymic:")
        await UserEdit.patronymic.set()
    if object == "Phonenumber":
        await call.message.answer("Enter phone_number:")
        await UserEdit.phone_number.set()


@dp.message_handler(state=UserEdit.name)
async def name(message: types.Message, state: FSMContext):
    factory.cursor.execute("UPDATE Profile SET name = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)


@dp.message_handler(state=UserEdit.surname)
async def name(message: types.Message, state: FSMContext):
    factory.cursor.execute("UPDATE Profile SET surname = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)


@dp.message_handler(state=UserEdit.patronymic)
async def name(message: types.Message, state: FSMContext):
    factory.cursor.execute("UPDATE Profile SET patronymic = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)


@dp.message_handler(state=UserEdit.phone_number)
async def name(message: types.Message, state: FSMContext):
    try:
        phone_number = phonenumbers.parse(message.text)
    except phonenumbers.NumberParseException:
        await message.answer(
            "Error! The phone number was entered incorrectly😔")
        return
    if not phonenumbers.is_possible_number(phone_number):
        await message.answer("Error! The phone number was entered incorrectly😔")
        return

    factory.cursor.execute("UPDATE Profile SET phone_number = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)
