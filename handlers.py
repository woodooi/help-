from aiogram import Router
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def start_handler(msg):
    pass
