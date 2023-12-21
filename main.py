import asyncio

from aiogram import Dispatcher

from help.elems.event.handlers.event_reg_handler import event_registration_router
from help.elems.user.handlers.user_reg_handler import router
from help.bot import bot


import logging
from help.elems.commands import set_commands
from help.elems.user.handlers.user_search_handler import search_musicians



async def main():
    dp = Dispatcher()
    dp.include_router(router)
    dp.include_router(event_registration_router)
    dp.include_router(search_musicians)
    await set_commands(bot)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())