
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage



# Configure logging
logging.basicConfig(level=logging.INFO)


# init
bot = Bot(token="5012647066:AAHrDpeucLHZ-mdVhS8t1KZBTFmw3NwGSjA", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())