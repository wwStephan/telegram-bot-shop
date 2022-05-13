import asyncio
from config import BOT_TOKEN
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

loop = asyncio.new_event_loop()
bot = Bot(BOT_TOKEN, parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, loop=loop, storage=storage)


async def shutdown(dp):
    await storage.close()


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_shutdown=shutdown)
