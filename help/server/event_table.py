from .db import events


async def add_event(event_name, event_date, event_location, event_description):

    event = {
        "event_name": event_name,
        "event_date": event_date,
        "event_location": event_location,
        "event_description": event_description
    }
    result = await events.insert_one(event)
    return result.inserted_id


async def get_all_events():
    result = await events.find().to_list(length=None)

    return result


