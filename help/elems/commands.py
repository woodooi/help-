from aiogram import Bot

from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description="Початок роботи"
        ),
        BotCommand(
            command='registration',
            description="Реєстрація музикантів"
        ),
        BotCommand(
            command='event_reg',
            description="Реєстрація подій"
        ),
        BotCommand(
            command='search_musicians',
            description="Пошук музикантів"
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())