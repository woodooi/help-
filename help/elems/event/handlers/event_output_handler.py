from aiogram import Router, types
from aiogram.filters import Command
from ...server import get_all_events


event_output_router = Router()


def format_event(event):
    formatted_text = (
        f"<b>event_name:</b> {event[1].get('event_name', '')}\n"
        f"<i>Date:</i> {event[1].get('event_date', '')}\n"
        f"<i>Location:</i> {event[1].get('event_location', '')}\n"
        f"<i>Description:</i> {event[1].get('event_description', '')}\n"
    )
    return formatted_text


@event_output_router.message(Command("event_output"))
async def get_all_events_handler(message: types.Message):
    events = await get_all_events()
    print(events)

    if events:
        for event in enumerate(events):
            formated_event = format_event(event)
            await message.answer(formated_event)
    else:
        await message.answer("Не має івентів")