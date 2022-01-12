
import logging
from Factory import Factory
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

PAYMENTS_PROVIDER_TOKEN = ''

bot = Bot(token="5064597537:AAHxPj8pwNhjLMmtaKWnae1evxOvqqrn-t4", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
factory = Factory("database.db")
