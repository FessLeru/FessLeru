import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from .filters import register_all_filters
from .misc import EnvKeys
from .handlers import register_all_handlers
from .database.models import register_models
from .logger_mesh import logger, file_handler

logger.addHandler(file_handler)


async def __on_start_up(dp: Dispatcher) -> None:
    register_all_filters(dp)
    register_all_handlers(dp)
    register_models()


async def start_bot():
    bot = Bot(token=EnvKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    print('Бот запущен')
    await __on_start_up(dp)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(start_bot())
