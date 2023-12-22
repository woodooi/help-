from .db import events


async def add_event(event_name, event_date, event_location, event_description, event_type):

    event = {
        "event_name": event_name,
        "event_date": event_date,
        "event_location": event_location,
        "event_description": event_description,
        "event_type": event_type
    }
    result = await events.insert_one(event)
    return result.inserted_id


async def get_all_events():
    result = await events.find().to_list(length=None)

    return result

async def find_events_type(city, event_type):
    query = {"event_location":city, "event_type": event_type}

    result = await events.find(query).to_list(length=None)

    return result


