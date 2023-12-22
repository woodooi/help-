from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..states.user_search_states import UserSearch
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from ...server import find_musicians_by_city_type

from .user_profile_handler import return_card
from .user_reg_handler import type_keyboard

search_musicians = Router()


@search_musicians.message(Command('search_musicians'))
async def start_search_handler(message: types.Message, state: FSMContext):
    await message.answer("Введи місто:")
    await state.set_state(UserSearch.WaitingForCity)


@search_musicians.message(UserSearch.WaitingForCity)
async def process_search_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    keyboard_for_search = ReplyKeyboardMarkup(keyboard=type_keyboard)
    await message.answer("Введи тип музиканта:", reply_markup=keyboard_for_search)
    await state.set_state(UserSearch.WaitingForType)


@search_musicians.message(UserSearch.WaitingForType)
async def process_search_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)

    data = await state.get_data()
    await state.clear()
    city = data.get("city")
    musician_type = data.get("type")

    musicians = await find_musicians_by_city_type(city, musician_type)

    if musicians:
        for musician in musicians:
            card = return_card(musician)
            await message.answer(card)
    else:
        await message.answer("No musicians found.", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))

