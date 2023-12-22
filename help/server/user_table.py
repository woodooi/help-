from .db import musicians


async def add_musician(musician_id, username, first_name, last_name, age, city, musician_type, pic, demo, description):

    existing_musician = await musicians.find_one({"$or": [{"musician_id": musician_id}, {"first_name": first_name, "last_name": last_name}]})
    if existing_musician:
        return None

    if not musician_id or not first_name or not last_name:
        return None

    musician = {
        "musician_id": musician_id,
        "username": username,
        "first_name": first_name,
        "last_name": last_name,
        "age": age,
        "city": city,
        "type": musician_type,
        "picture": pic,
        "demo": demo,
        "description": description
    }

    result = await musicians.insert_one(musician)

    return result.inserted_id


async def find_self_by_id(musician_id):
    musician = await musicians.find_one({"musician_id": musician_id})

    return musician 


async def find_musicians_by_city_type(city, musician_type):
    query = {"city": city, "type": musician_type}

    result = await musicians.find(query).to_list(length=None)

    return result


async def update_musician(chat_id, field, new_value):
    musician = musicians.find_one({"musician_id": chat_id})

    if musician:
        musicians.update_one(
            {"musician_id": chat_id},
            {"$set": {field: new_value}}
        )
        return True
    else:
        return False




