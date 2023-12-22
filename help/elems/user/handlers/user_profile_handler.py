from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import BufferedInputFile, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from io import BytesIO
from aiogram.types import Audio, Voice

from ...server import find_self_by_id
from ..states.user_edit_states import UserEdit
from ..states.user_reg_states import UserRegistration
from ....server.user_table import musicians

profile_router = Router()

fields = ["first_name", "last_name", "age", "city", "type", "description"]

keyboard_fields = [
    [KeyboardButton(text=field) for field in fields]
]

def return_card(musician):
    
    formatted_text = (
        f"<b>|#| Музи́ка: {musician.get('first_name', '')} {musician.get('last_name', '')}</b>\n"
        f"<b>|#| Вік:</b> {musician.get('age', '')}\n"
        f"<b>|#| Місто:</b> {musician.get('city', '')}\n"
        f"<b>|#| Масть:</b> {musician.get('type', '')}\n"
        f"<b>|#| Про себе:</b> {musician.get('description', '')}\n"
        f"<b>|#| Ось @{musician.get('username', '')} - гарної вам гри!</b>"
    )

    return formatted_text

@profile_router.message(Command("profile"), F.text)
async def show_your_profile(message: types.Message):
    musician = await find_self_by_id(message.from_user.id)
    card = return_card(musician)
    await message.answer_photo(musician.get('picture', ''))
    await message.answer(card, parse_mode="HTML")
    demo = musician.get('demo', '')
    if type(demo) == Audio:
        await message.answer_audio(demo, caption="їх гра!")
    elif type(demo) == Voice:
        await message.answer_voice(demo, caption="їх гра!")

@profile_router.message(Command("edit_profile"), F.text)
async def start_edit_profile(message:types.Message, state:FSMContext):
    options = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=keyboard_fields)
    await message.answer("Що ви хочете змінити?", reply_markup=options)
    await state.set_state(UserEdit.WaitingForTarget)

@profile_router.message(UserEdit.WaitingForTarget)
async def process_editing(message:types.Message, state:FSMContext):
    if message.text == "age":
        await message.answer("З днем народження!")
    await state.update_data(target_field=message.text)
    await message.answer("Введіть нове значення", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(UserEdit.WaitingForQuery)

@profile_router.message(UserEdit.WaitingForQuery)
async def editing(message:types.Message, state:FSMContext):
    await state.update_data(new_value=message.text)
    data = await state.get_data()
    await state.clear()

    find_my_profile = {"musician_id": message.from_user.id}

    edit = {"$set": {str(data["target_field"]): data["new_value"]}} #probably doesn`t work, also need to fix 
                                                                    #button names or solve this problemik
                                                                    #seems to work, hz)
    result = musicians.update_one(find_my_profile, edit)
    if result:
        await message.answer("Updated_successfully")   
    return result
