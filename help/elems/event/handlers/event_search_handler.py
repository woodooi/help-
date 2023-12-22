from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..states.event_search_states import Search
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove

from ....server.event_table import find_events_type
from ..states.event_search_states import Search
from .event_output_handler import format_event
from .event_reg_handler import event_type_opt


search_event = Router()

@search_event.message(Command("event_search"))
async def start_event_search(message:types.Message, state: FSMContext):
    await message.answer("Start searching enter type:", reply_markup=ReplyKeyboardMarkup(keyboard=event_type_opt, resize_keyboard=True))
    await state.set_state(Search.WaitingForType)

@search_event.message(Search.WaitingForType)
async def process_type(message:types.Message, state: FSMContext):
    await state.update_data(event_type=message.text)
    await message.answer("Введіть місто:", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(Search.WaitingForCity)

@search_event.message(Search.WaitingForCity)
async def process_query(message:types.Message, state:FSMContext):
    await state.update_data(event_city=message.text)

    data = await state.get_data()
    await state.clear()
    event_type = data['event_type']
    city = data['event_city']

    events = await find_events_type(city, event_type)

    if events:
       for event in enumerate(events):
            formated_event = format_event(event)
            await message.answer(formated_event)
    else:
        await message.answer("Не має івентів") 
