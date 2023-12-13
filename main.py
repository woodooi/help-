import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from handlers import router

import logging

TOKEN = "6336804169:AAHYI8xf4XR5gSvf7W-Pc0c3ePr2tzkeSrU"


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())