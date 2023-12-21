from db import events


async def add_event(event_name, event_date, event_location, event_description):

    event = {
        "event_name": event_name,
        "event_date": event_date,
        "event_location": event_location,
        "event_description": event_description
    }
    print(event)
    result = await events.insert_one(event)
    return result.inserted_id

