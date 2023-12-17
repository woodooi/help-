import motor.motor_asyncio


cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://kozlobogdann:NRBHiJcL5uHvDAEI@cluster0.npttskr.mongodb.net/?retryWrites=true&w=majority")

collection = cluster.Help_Musician_DB.user


async def add_musician(demo, pic, description):

    musician = {
       "demo":  demo,
       "pic": pic,
       "description": description
    }

    result = await collection.insert_one(musician)

    return result.inserted_id

async def add_event(event_name, event_date, event_location, event_description):

    # existing_event = await collection.find_one({})
    if not event_name or event_date or event_description:
        return None
    
    event = {
        "event_name":event_name,
        "event_date":event_date,
        "event_location":event_location,
        "event_description": event_description
    }

    result = await collection.insert_one(event)
    return result.inserted_id
    