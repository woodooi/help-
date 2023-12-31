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
        ),
        BotCommand(
            command='event_output',
            description="Всі події"
        ),
        BotCommand(
            command="profile",
            description="Ваш профіль"
        ),
        BotCommand(
            command="event_search",
            description="знайти івент за параметрами"
        ),
        BotCommand(
            command="edit_profile",
            description="змінити значення поля профілю"
        )
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeDefault())