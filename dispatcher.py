
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

PAYMENTS_PROVIDER_TOKEN = '1744374395:TEST:593e0b74638f2497dba0'

bot = Bot(token="5069171978:AAGVq-SqVTS6oD0zy0ECz6OZf6N2LHqqOTI", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
