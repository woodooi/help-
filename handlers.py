from io import BytesIO
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile
from pydub import AudioSegment

from typing import BinaryIO

from db import add_musician
from registration import Registration

from bot import bot

router = Router()

@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Вас вітає реєстраційний бот для музикантів! Давайте розпочнемо.")
    await message.answer("Демо:")
    await state.set_state(Registration.WaitingForDemo) 

@router.message(Registration.WaitingForDemo)
async def process_demo(message: types.Message, state: FSMContext):
    if message.voice:
        file_id = message.voice.file_id
        await state.update_data(demo=file_id)
        await message.answer_voice(file_id)
        await state.set_state(Registration.WaitingForPic)
    elif message.audio:
        file_id = message.audio.file_id
        await state.update_data(demo=file_id)
        await message.answer_audio(file_id)
        await state.set_state(Registration.WaitingForPic)
    await message.answer("Photo")

@router.message(Registration.WaitingForPic)
async def process_pic(message: types.Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[0].file_id
        await state.update_data(pic=file_id)
        await state.update_data(pic=file_id)
        await state.set_state(Registration.WaitingForDescription)
    elif message.document:
        photo = await bot.download(message.document, BytesIO())
        input_photo = BufferedInputFile(photo.getvalue(), message.document.file_name)
        await state.update_data(pic=input_photo)
        await message.answer_photo(input_photo)
        await state.set_state(Registration.WaitingForDescription)
    elif message.text:
        await message.answer("Натисни на скріпку, там мають бути фото")  

@router.message(Registration.WaitingForDescription)
async def process_description(message: types.Message, state: FSMContext):
    data = await state.get_data()
    result = await add_musician(data['demo'], data['pic'], message.text)
    if result:
        await message.answer(f"Ви успішно зареєстровані як музикант з ID: {result}")
    else:
        await message.answer("Не вдалося зареєструвати музиканта. Будь ласка, спробуйте знову.")