from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from dispatcher import factory

from Factory import Factory
from dispatcher import dp, bot
from files.authorization import cancel
from files.bot import kb

# factory = Factory("database.db")


class UserFilter(StatesGroup):
    begin = State()
    end = State()


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


async def create_button(call, name):
    ft = ReplyKeyboardMarkup()
    ft.add(KeyboardButton("Сортувати за ціною"))
    ft.add(KeyboardButton("Повернутись у меню"))
    await bot.send_message(call.from_user.id, "Оберіть:", reply_markup=ft)

    @dp.message_handler(text="Сортувати за ціною")
    async def callback(message: types.Message):
        await message.answer(text="Нижня межа ціни:",
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).row(KeyboardButton("🔙Назад")))
        await UserFilter.begin.set()

    @dp.message_handler(state=UserFilter.begin)
    async def surname_input(message: types.Message, state: FSMContext):
        if message.text == "🔙Назад":
            await cancel(message, state)
            return
        try:
            number_begin = int(message.text)
        except:
            await message.answer("Нижня межа ціни повинна бути числом😔")
            return
        if number_begin < 0:
            await message.answer("Нижня межа ціни повинна бути більшою нуля😔")
            return
        await state.update_data(begin=number_begin)
        await message.answer("Верхня межа ціни:")
        await UserFilter.end.set()

    @dp.message_handler(state=UserFilter.end)
    async def surname_input(message: types.Message, state: FSMContext):
        if message.text == "🔙Назад":
            await cancel(message, state)
            return
        try:
            number_end = int(message.text)
        except:
            await message.answer("Верхня межа ціни повинна бути числом😔")
            return
        if number_end < 0:
            await message.answer("Верхня межа ціни повинна бути більшою нуля😔")
            return
        number = await state.get_data()
        if number["begin"] > number_end:
            await message.answer("Верхня межа ціни повинна бути більша нижньої😔")
            return
        await state.update_data(end=number_end)
        await sql_read(message, name, await state.get_data())
        await state.finish()


@dp.callback_query_handler(text="Accessories_man")
async def send_accessories(call: CallbackQuery):
    await sql_read(call, 'Accessories_man')
    await create_button(call, 'Accessories_man')


@dp.callback_query_handler(text="Accessories_woman")
async def send_accessories(call: CallbackQuery):
    await sql_read(call, 'Accessories_woman')
    await create_button(call, 'Accessories_woman')


@dp.callback_query_handler(text="Outerwear_man")
async def send_outerwear(call: CallbackQuery):
    await sql_read(call, 'Outerwear_man')
    await create_button(call, 'Outerwear_man')


@dp.callback_query_handler(text="Outerwear_woman")
async def send_outerwear(call: CallbackQuery):
    await sql_read(call, 'Outerwear_woman')
    await create_button(call, 'Outerwear_woman')


@dp.callback_query_handler(text="Hoodies_man")
async def send_hoodies(call: CallbackQuery):
    await sql_read(call, 'Hoodies_man')
    await create_button(call, 'Hoodies_man')


@dp.callback_query_handler(text="Hoodies_woman")
async def send_hoodies(call: CallbackQuery):
    await sql_read(call, 'Hoodies_woman')
    await create_button(call, 'Hoodies_woman')


@dp.callback_query_handler(text="Accessories_woman")
async def send_accessories(call: CallbackQuery):
    await sql_read(call, 'Accessories_woman')
    await create_button(call, 'Accessories_woman')


@dp.callback_query_handler(text="Pants_man")
async def send_pants(call: CallbackQuery):
    await sql_read(call, 'Pants_man')
    await create_button(call, 'Pants_man')


@dp.callback_query_handler(text="Pants_woman")
async def send_pants(call: CallbackQuery):
    await sql_read(call, 'Pants_woman')
    await create_button(call, 'Pants_woman')


@dp.callback_query_handler(text="Underwear_man")
async def send_underwear(call: CallbackQuery):
    await sql_read(call, 'Underwear_man')
    await create_button(call, 'Underwear_man')


@dp.callback_query_handler(text="Underwear_woman")
async def send_underwear(call: CallbackQuery):
    await sql_read(call, 'Underwear_woman')
    await create_button(call, 'Underwear_woman')


def get_name_product_by_id(id_product):
    result = factory.cursor.execute("SELECT * FROM Product WHERE idProduct = ?", (id_product,)).fetchone()
    return result[1]


async def sql_add_command(id_element, id_user):
    id_elements = factory.cursor.execute("SELECT * FROM Basket WHERE idProfile = ? AND idProduct = ?",
                                         (id_user, id_element)).fetchone()
    if id_elements is None:
        factory.cursor.execute('INSERT INTO Basket (idProfile, idProduct) VALUES (?,?);', (id_user, id_element))
        factory.connector.commit()
        return True
    else:
        return False


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('add '))
async def add_callback_run(callback_query: types.CallbackQuery):
    if await sql_add_command(callback_query.data.replace('add ', ''), callback_query.from_user.id):
        await callback_query.answer(text=f"{get_name_product_by_id(callback_query.data.replace('add ', ''))} додано.",
                                    show_alert=True)
    else:
        await callback_query.answer(
            text=f"{get_name_product_by_id(callback_query.data.replace('add ', ''))} вже є у Вашій корзині.", show_alert=True)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('like '))
async def add_callback_run(callback_query: types.CallbackQuery):
    temp = factory.cursor.execute("SELECT * FROM Ordering WHERE pay = 1 AND idProfile =:currIdProfile AND idFull in "
                                  "(SELECT idFull from FullProduct where idProduct =:currId)",
                                  {"currIdProfile": callback_query.from_user.id,
                                   "currId": callback_query.data.replace('like ', '')}).fetchone()
    if temp is not None:
        review = factory.cursor.execute("SELECT * FROM Reviews WHERE idProduct = :currId AND idProfile =:currIdProfile",
                                        {"currId": callback_query.data.replace('like ', ''),
                                         "currIdProfile": callback_query.from_user.id}).fetchone()
        if review is None:
            factory.cursor.execute("INSERT INTO Reviews (idProduct, idProfile, likes, dislikes) VALUES (?,?,?,?);",
                                   (callback_query.data.replace('like ', ''),
                                    callback_query.from_user.id, 1, 0))
            factory.connector.commit()
            await callback_query.answer(
                text=f"Like for {get_name_product_by_id(callback_query.data.replace('like ', ''))}"
                     f" added.", show_alert=True)
        else:
            await callback_query.answer(text=f"Ви вже додали відгук на цей товар!", show_alert=True)
    else:
        await callback_query.answer(text=f"Ви не можете додати відгук без покупки товару!", show_alert=True)


@dp.callback_query_handler(lambda x: x.data and x.data.startswith('dislike '))
async def add_callback_run(callback_query: types.CallbackQuery):
    temp = factory.cursor.execute("SELECT * FROM Ordering WHERE pay = 1 AND idProfile =:currIdProfile AND idFull in "
                                  "(SELECT idFull from FullProduct where idProduct =:currId)",
                                  {"currIdProfile": callback_query.from_user.id,
                                   "currId": callback_query.data.replace('like ', '')}).fetchone()
    if temp is None:
        review = factory.cursor.execute("SELECT * FROM Reviews WHERE idProduct = :currId AND idProfile =:currIdProfile",
                                        {"currId": callback_query.data.replace('dislike ', ''),
                                         "currIdProfile": callback_query.from_user.id}).fetchone()
        if review is None:
            factory.cursor.execute("INSERT INTO Reviews VALUES (?,?,?,?);", (callback_query.data.replace('like ', ''),
                                                                             callback_query.from_user.id, 0, 1))
            factory.connector.commit()
            await callback_query.answer(
                text=f"👍 для {get_name_product_by_id(callback_query.data.replace('dislike ', ''))}"
                     f" додано.", show_alert=True)
        else:
            await callback_query.answer(text=f"Ви вже додали відгук на цей товар!", show_alert=True)
    else:
        await callback_query.answer(text=f"Ви не можете додати відгук без покупки товару!", show_alert=True)


async def sql_read(message, type_clothes, filter_price=None):
    if filter_price is None:
        products = [factory.select_by_id_db(i[0]) for i in
                    factory.cursor.execute("SELECT * FROM Product WHERE type = :typeCl",
                                           {"typeCl": type_clothes}).fetchall()]
    else:
        products = [factory.select_by_id_db(i[0]) for i in
                    factory.cursor.execute("SELECT * FROM Product WHERE type = :typeCl AND price>=:state_begin AND "
                                           "price<=:state_end", {"typeCl": type_clothes,
                                                                 "state_begin": filter_price["begin"],
                                                                 "state_end": filter_price["end"]}).fetchall()]
    if not len(products):
        await message.answer("Порожня категорія...")
    else:
        for product in products:
            reviews = factory.cursor.execute("SELECT * FROM Reviews WHERE idProduct = :currId",
                                             {"currId": product[0]}).fetchone()
            await bot.send_photo(message.from_user.id, photo=product[5])
            if reviews is not None:
                likes = factory.cursor.execute("SELECT COUNT(*) FROM Reviews WHERE idProduct = :currId AND likes = 1",
                                               {"currId": product[0]}).fetchone()[0]
                dislikes = \
                    factory.cursor.execute("SELECT COUNT(*) FROM Reviews WHERE idProduct = :currId AND dislikes = 1",
                                           {"currId": product[0]}).fetchone()[0]
                await bot.send_message(message.from_user.id, f'👍: {likes}, 👎: {dislikes}')
            await bot.send_message(message.from_user.id, f'{product[1]}\nОпис: {product[2]}\n'
                                                         f'Ціна: {product[3]}\n',
                                   reply_markup=InlineKeyboardMarkup().add(
                                       InlineKeyboardButton(f'Додати в корзину {product[1]}',
                                                            callback_data=f'add {product[0]}')).add(
                                       InlineKeyboardButton(f'Лайкнути {product[1]}',
                                                            callback_data=f'like {product[0]}')).add(
                                       InlineKeyboardButton(f'Дізлайкнути {product[1]}',
                                                            callback_data=f'dislike {product[0]}')))
