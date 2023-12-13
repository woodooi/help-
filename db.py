import motor.motor_asyncio


cluster = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://kozlobogdann:NRBHiJcL5uHvDAEI@cluster0.npttskr.mongodb.net/?retryWrites=true&w=majority")

collection = cluster.Help_Musician_DB.user


async def add_musician(musician_id, first_name, last_name, age, city, musician_type, description):

    existing_musician = await collection.find_one({"$or": [{"musician_id": musician_id}, {"first_name": first_name, "last_name": last_name}]})
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

    result = await collection.insert_one(musician)

    return result.inserted_id

