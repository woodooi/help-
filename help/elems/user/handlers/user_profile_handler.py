from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import BufferedInputFile
from io import BytesIO
from aiogram.types import Audio, Voice

from ...server import find_self_by_id

profile_router = Router()

def return_card(musician):
    
    formatted_text = (
        f"<b>|#| Музи́ка: {musician.get('first_name', '')} {musician.get('last_name', '')}</b>\n"
        f"<b>|#| Вік:</b> {musician.get('age', '')}\n"
        f"<b>|#| Місто:</b> {musician.get('city', '')}\n"
        f"<b>|#| Масть:</b> {musician.get('type', '')}\n"
        f"<b>|#| Про себе:</b> {musician.get('description', '')}\n"
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
