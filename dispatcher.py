
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage



# Configure logging
logging.basicConfig(level=logging.INFO)


# init
bot = Bot(token="2113090286:AAFXEnCPZIaQWBMhl9ohr5soUtXcKALMYqw", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())