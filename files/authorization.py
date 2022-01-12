
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dispatcher import factory as factory
from files.bot import kb
import phonenumbers

from dispatcher import dp




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
change.row(KeyboardButton("Так"), KeyboardButton("Ні"))


@dp.message_handler(commands=['reg'])
async def register_start(message: types.Message):
    await message.answer("Привіт! Введи своє прізвище:",
                         reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("🔙 Повернутись в головне меню")))
    await UserRegister.surname.set()


@dp.message_handler(state=UserRegister.surname)
async def surname_input(message: types.Message, state: FSMContext):
    if message.text == "🔙 Повернутись в головне меню":
        await cancel(message, state)
        return
    await state.update_data(surname=message.text)
    await message.answer("Введіть ім'я:")
    await UserRegister.name.set()


@dp.message_handler(state=UserRegister.name)
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


@dp.message_handler(state=UserRegister.phone_number)
async def phone_number_input(message: types.Message, state: FSMContext):
    if message.text == "🔙 Повернутись в головне меню":
        await cancel(message, state)
        return
    try:
        phone_number = phonenumbers.parse(message.text)
    except phonenumbers.NumberParseException:
        await message.answer(
            "Помилка! Ваш номер телефону неправльно введений😔")
        return
    if not phonenumbers.is_possible_number(phone_number):
        await message.answer("Помилка! Ваш номер телефону неправльно введений😔")
        return

    await state.update_data(phone_number=message.text)
    new_user = await state.get_data()

    sql = f"UPDATE Profile SET surname = ?, name = ?, patronymic = ?, phone_number = ? WHERE id = ?;"
    data = (new_user["surname"], new_user["name"], new_user["patronymic"], new_user["phone_number"], message.from_user.id)
    factory.cursor.execute(sql, data)
    factory.connector.commit()
    await message.answer("Реєстрацію завершено✅")
    await state.finish()
    await profile(message)


@dp.message_handler(Text(equals="🔙 Повернутись в головне меню"))
async def cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Виберіть дію",
                         reply_markup=kb)


@dp.message_handler(lambda message: message.text == "Профіль🙎‍♂️🙍‍♀️")
async def profile(message: types.Message):
    if my_profile(message.from_user.id):
        await message.answer(my_profile(message.from_user.id), reply_markup=change)
    else:
        await message.answer("У вас немає профілю зареєструйтесь будь ласка")
        await register_start(message)


def my_profile(id):
    profiles = factory.cursor.execute(f"SELECT * FROM Profile WHERE id = {id};").fetchall()
    for profile in profiles:
        if profile[1]:
            return f"Ваш профіль :\nІм'я: {profile[1]}\nПрізвище: {profile[2]}\nПо батькові: {profile[3]}\nНомер телефону: {profile[4]}\nВи хочете змінити профіль?"
        else:
            return None


@dp.message_handler(text="Ні")
async def no(message: types.Message):
    await message.answer("Виберіть операцію", reply_markup=kb)


@dp.message_handler(text="Відмінити")
async def otmena(message: types.Message, state: FSMContext):
    await state.finish()
    await profile(message)


@dp.message_handler(text="Так")
async def yes(message: types.Message):
    edits = InlineKeyboardMarkup()
    edits.add(InlineKeyboardButton(text="Ім'я", callback_data="edit_Name"))
    edits.add(InlineKeyboardButton(text="Прізвище", callback_data="edit_Surname"))
    edits.add(InlineKeyboardButton(text="По батькові", callback_data="edit_Patronymic"))
    edits.add(InlineKeyboardButton(text="Номер телефону", callback_data="edit_Phonenumber"))
    await message.answer("Виберіть, що вихочете змінити:", reply_markup=edits)


@dp.callback_query_handler(lambda call: call.data.startswith('edit'))
async def callback_worker_promo(call: CallbackQuery):
    model_type, object = call.data.split("_")
    if object == "Name":
        await call.message.answer("Введіть ім'я:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Відмінити")))
        await UserEdit.name.set()
    if object == "Surname":
        await call.message.answer("Введіть прізвище:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Відмінити")))
        await UserEdit.surname.set()
    if object == "Patronymic":
        await call.message.answer("Введіть по батькові:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Відмінити")))
        await UserEdit.patronymic.set()
    if object == "Phonenumber":
        await call.message.answer("Введіть номер телефону:", reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("Відмінити")))
        await UserEdit.phone_number.set()


@dp.message_handler(state=UserEdit.name)
async def name(message: types.Message, state: FSMContext):
    if message.text == "Відмінити":
        await otmena(message,state)
        return
    factory.cursor.execute("UPDATE Profile SET name = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)


@dp.message_handler(state=UserEdit.surname)
async def name(message: types.Message, state: FSMContext):
    if message.text == "Відмінити":
        await otmena(message,state)
        return
    factory.cursor.execute("UPDATE Profile SET surname = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)


@dp.message_handler(state=UserEdit.patronymic)
async def name(message: types.Message, state: FSMContext):
    if message.text == "Відмінити":
        await otmena(message,state)
        return
    factory.cursor.execute("UPDATE Profile SET patronymic = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)


@dp.message_handler(state=UserEdit.phone_number)
async def name(message: types.Message, state: FSMContext):
    if message.text == "Відмінити":
        await otmena(message,state)
        return
    try:
        phone_number = phonenumbers.parse(message.text)
    except phonenumbers.NumberParseException:
        await message.answer(
            "Помилка! Ваш номер телефону неправльно введений😔")
        return
    if not phonenumbers.is_possible_number(phone_number):
        await message.answer("Помилка! Ваш номер телефону неправльно введений😔")
        return

    factory.cursor.execute("UPDATE Profile SET phone_number = ? WHERE id = ?;", (message.text, message.from_user.id))
    factory.connector.commit()
    await state.finish()
    await profile(message)
