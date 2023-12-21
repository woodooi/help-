from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db import add_event
from event_registration import EventRegistration

event_registration_router = Router()


@event_registration_router.message(Command("event_reg"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Введіть назву")
    await state.set_state(EventRegistration.WaitingForName)


@event_registration_router.message(EventRegistration.WaitingForName)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await message.answer("Введiть дату")
    await state.set_state(EventRegistration.WaitingForDate)


@event_registration_router.message(EventRegistration.WaitingForDate)
async def set_descript(message: types.Message, state: FSMContext):
    await state.update_data(event_date=message.text)
    await message.answer("Введіть локацію ")
    await state.set_state(EventRegistration.WaitingForLocation)


@event_registration_router.message(EventRegistration.WaitingForLocation)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(event_location=message.text)
    await message.answer("Введіть опис")
    await state.set_state(EventRegistration.WaitingForDescription)


@event_registration_router.message(EventRegistration.WaitingForDescription)
async def set_date(message: types.Message, state: FSMContext):
    await state.update_data(event_description=message.text)
    data = await state.get_data()
    event_to_add = await add_event(data['event_name'], data['event_date'], data['event_location'],
                                   data['event_description'])
    if event_to_add:
        return await message.answer(f"Подію зареєстровано:{event_to_add}")
    else:
        return await message.answer("сорян")