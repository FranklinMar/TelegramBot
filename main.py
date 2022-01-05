
from aiogram.utils import executor
from dispatcher import dp
from files.delete_ordering import on_startup


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=False, on_startup=on_startup)
