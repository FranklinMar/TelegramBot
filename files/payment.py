import asyncio
import logging
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import sqlite3 as sq

from DatabaseFunctions import select_by_id_db
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.types.message import ContentType
from dispatcher import dp, bot, PAYMENTS_PROVIDER_TOKEN
from messages import MESSAGES


logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.INFO)


loop = asyncio.get_event_loop()
# bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
# dp = Dispatcher(bot, loop=loop)

# Setup prices
PRICES = [
    types.LabeledPrice(label='Product', amount=4200000),
    types.LabeledPrice(label='Product', amount=30000)
]

# Setup shipping options
DEFAULT_SHIPPING_OPTION = types.ShippingOption(
    id='default',
    title='Нова пошта'
).add(types.LabeledPrice('Нова пошта', 1000000))

UKRAINE_POST_SHIPPING_OPTION = types.ShippingOption(
    id='uk_post', title='Укр пошта')

UKRAINE_POST_SHIPPING_OPTION.add(
    types.LabeledPrice(
        'Укр пошта', 100000)
)

PICKUP_SHIPPING_OPTION = types.ShippingOption(id='pickup', title='Самовивіз')
PICKUP_SHIPPING_OPTION.add(types.LabeledPrice('Самовивіз', 50000))


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(MESSAGES['start'])


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])


@dp.message_handler(commands=['terms'])
async def process_terms_command(message: types.Message):
    await message.reply(MESSAGES['terms'], reply=False)


@dp.message_handler(commands=['buy'])
async def process_buy_command(message: types.Message):
    if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, MESSAGES['pre_buy_demo_alert'])

    await bot.send_invoice(message.chat.id,
                           title=MESSAGES['tm_title'],
                           description=MESSAGES['tm_description'],
                           provider_token=PAYMENTS_PROVIDER_TOKEN,
                           currency='rub',

                           photo_height=512,  # !=0/None or picture won't be shown
                           photo_width=512,
                           photo_size=512,
                           need_email=True,
                           need_phone_number=True,
                           # need_shipping_address=True,
                           is_flexible=True,  # True If you need to set up Shipping Fee
                           prices=PRICES,
                           start_parameter='time-machine-example',
                           payload='some-invoice-payload-for-our-internal-use')


@dp.shipping_query_handler(lambda query: True)
async def process_shipping_query(shipping_query: types.ShippingQuery):
    print('shipping_query.shipping_address')
    print(shipping_query.shipping_address)

    if shipping_query.shipping_address.country_code == 'AU':
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message=MESSAGES['AU_error']
        )

    shipping_options = [DEFAULT_SHIPPING_OPTION]

    if shipping_query.shipping_address.country_code == 'UA':
        shipping_options.append(UKRAINE_POST_SHIPPING_OPTION)

        if shipping_query.shipping_address.city == 'Київ':
            shipping_options.append(PICKUP_SHIPPING_OPTION)

    await bot.answer_shipping_query(
        shipping_query.id,
        ok=True,
        shipping_options=shipping_options
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print('order_info')
    print(pre_checkout_query.order_info)

    if hasattr(pre_checkout_query.order_info, 'email'):
        return await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message=MESSAGES['wrong_email'])

    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    await bot.send_message(
        message.chat.id,
        MESSAGES['successful_payment'].format(
            total_amount=message.successful_payment.total_amount // 100,
            currency=message.successful_payment.currency
        )
    )


if __name__ == '__main__':
    executor.start_polling(dp, loop=loop)