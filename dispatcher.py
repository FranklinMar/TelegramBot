
import logging
from Factory import Factory
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

PAYMENTS_PROVIDER_TOKEN = '1744374395:TEST:acf2e035a6ab38459323'

bot = Bot(token="5040947022:AAF0wrj3xr94XqkFggMjjWh4qqFPU9FC32U", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
factory = Factory("database.db")
