from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from event_search import EventSearch

from db import find_musicians_by_city_type

search_musicians = Router()


def format_musician(index, musician):
    formatted_text = (
        f"<b>Musician #{index}</b>\n"
        f"<i>Name:</i> {musician.get('first_name', '')} {musician.get('last_name', '')}\n"
        f"<i>Age:</i> {musician.get('age', '')}\n"
        f"<i>City:</i> {musician.get('city', '')}\n"
        f"<i>Type:</i> {musician.get('type', '')}\n"
        f"<i>Description:</i> {musician.get('description', '')}\n"
    )
    return formatted_text


@search_musicians.message(Command('search_musicians'))
async def start_search_handler(message: types.Message, state: FSMContext):
    await message.answer("Введи місто:")
    await state.set_state(EventSearch.WaitingForCity)


@search_musicians.message(EventSearch.WaitingForCity)
async def process_search_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)

    await message.answer("Введи тип музиканта:")
    await state.set_state(EventSearch.WaitingForType)


@search_musicians.message(EventSearch.WaitingForType)
async def process_search_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)

    data = await state.get_data()
    city = data.get("city")
    musician_type = data.get("type")

    musicians = await find_musicians_by_city_type(city, musician_type)

    if musicians:
        for index, musician in enumerate(musicians):
            formatted_musician = format_musician(index + 1, musician)
            await message.answer(formatted_musician)
    else:
        await message.answer("No musicians found.")

