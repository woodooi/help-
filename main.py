import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from event_heandlers import event_registration_router
from event_reg_handler import router
from handlers import bot

import logging

from search_hendler import search_musicians




async def main():
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(event_registration_router)
    dp.include_router(search_musicians)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())