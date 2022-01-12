import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

PAYMENTS_PROVIDER_TOKEN = '1744374395:TEST:7c8b4dfb1271ef0a0486'

bot = Bot(token="5018134318:AAGwrYz-eJWqK1KsgXDXVEq7Ge-dNBHWVQM", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())