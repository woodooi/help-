import motor.motor_asyncio


cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://kozlobogdann:NRBHiJcL5uHvDAEI@cluster0.npttskr.mongodb.net/?retryWrites=true&w=majority")

musicians = cluster.Help_Musician_DB.user
events = cluster.Help_Musician_DB.events


async def add_musician(musician_id, first_name, last_name, age, city, musician_type, description):

    existing_musician = await musicians.find_one({"$or": [{"musician_id": musician_id}, {"first_name": first_name, "last_name": last_name}]})
    if existing_musician:
        return None

    if not musician_id or not first_name or not last_name:
        return None

    musician = {
        "musician_id": musician_id,
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "city": city,
        "type": musician_type,
        "description": description
    }

    result = await musicians.insert_one(musician)

    return result.inserted_id


async def is_musician_registered(musician_id):
    musician = await musicians.find_one({"musician_id": musician_id})

    return musician is not None


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


async def find_musicians_by_city_type(city, musician_type):
    query = {"city": city, "type": musician_type}

    result = await musicians.find(query).to_list(length=None)

    return result
