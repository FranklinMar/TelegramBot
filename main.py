from aiogram.utils import executor
from dispatcher import dp
import files

if __name__ == "__main__":
    executor.start_polling(dp)
