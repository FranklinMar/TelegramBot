from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

TOKEN = '2113090286:AAFXEnCPZIaQWBMhl9ohr5soUtXcKALMYqw'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

kb = ReplyKeyboardMarkup()
kb.add(KeyboardButton('Реєcтpація'))
kb.add(KeyboardButton('Каталог'))
kb.add(KeyboardButton('Корзина'))
kb.add(KeyboardButton('Інформація'))
kb.add(KeyboardButton('Допомога'))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!", reply_markup=kb)


@dp.message_handler(lambda message: message.text == "Каталог")
async def send_catalog(message: types.Message):
    kt = ReplyKeyboardMarkup()
    kt.add(KeyboardButton("Жіночий одяг"))
    kt.add(KeyboardButton('Чоловічий одяг'))
    kt.add(KeyboardButton('Дитячий одяг'))
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


@dp.message_handler(text="Дитячий одяг")
async def send_child(message: types.Message):
    children = InlineKeyboardMarkup()
    children.add(InlineKeyboardButton(text="Верхній одяг", callback_data="Outerwear_child"))
    children.add(InlineKeyboardButton(text="Толстовки", callback_data="Hoodies_child"))
    children.add(InlineKeyboardButton(text="Аксесуари", callback_data="Accessories_child"))
    children.add(InlineKeyboardButton(text="Штани", callback_data="Pants_child"))
    children.add(InlineKeyboardButton(text="Білизна", callback_data="Underwear_child"))
    await message.answer("Оберіть:", reply_markup=children)


@dp.callback_query_handler(text="Accessories_man")
async def send_accessories(call: CallbackQuery):
    await call.message.answer("Accessories_man")


@dp.callback_query_handler(text="Accessories_child")
async def send_accessories(call: CallbackQuery):
    await call.message.answer("Accessories_child")


@dp.callback_query_handler(text="Outerwear_man")
async def send_outerwear(call: CallbackQuery):
    await call.message.answer("Outerwear_man")


@dp.callback_query_handler(text="Outerwear_woman")
async def send_outerwear(call: CallbackQuery):
    await call.message.answer("Outerwear_woman")


@dp.callback_query_handler(text="Outerwear_child")
async def send_outerwear(call: CallbackQuery):
    await call.message.answer("Outerwear_child")


@dp.callback_query_handler(text="Hoodies_man")
async def send_hoodies(call: CallbackQuery):
    await call.message.answer("Hoodies_man")


@dp.callback_query_handler(text="Hoodies_woman")
async def send_hoodies(call: CallbackQuery):
    await call.message.answer("Hoodies_woman")


@dp.callback_query_handler(text="Hoodies_child")
async def send_hoodies(call: CallbackQuery):
    await call.message.answer("Hoodies_child")


@dp.callback_query_handler(text="Accessories_woman")
async def send_accessories(call: CallbackQuery):
    await call.message.answer("Accessories_woman")


@dp.callback_query_handler(text="Pants_man")
async def send_pants(call: CallbackQuery):
    await call.message.answer("Pants_man")


@dp.callback_query_handler(text="Pants_woman")
async def send_pants(call: CallbackQuery):
    await call.message.answer("Pants_woman")


@dp.callback_query_handler(text="Pants_child")
async def send_pants(call: CallbackQuery):
    await call.message.answer("Pants_child")


@dp.callback_query_handler(text="Underwear_man")
async def send_underwear(call: CallbackQuery):
    await call.message.answer("Underwear_man")


@dp.callback_query_handler(text="Underwear_woman")
async def send_underwear(call: CallbackQuery):
    await call.message.answer("Underwear_woman")


@dp.callback_query_handler(text="Underwear_child")
async def send_underwear(call: CallbackQuery):
    await call.message.answer("Underwear_child")


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


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text, reply_markup=kb)

executor.start_polling(dp)
