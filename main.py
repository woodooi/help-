import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from event_heandlers import event_registration_router
from handlers import router

import logging

from search_hendler import search_musicians

TOKEN = "6864353551:AAHIZ8GAxLo2K1NPo0Y_gUOvBnnJvS3WO1U"


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(event_registration_router)
    dp.include_router(search_musicians)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())