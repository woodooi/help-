from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import BufferedInputFile
from io import BytesIO

from handlers import bot

from db import add_musician, is_musician_registered
from registration import Registration

router = Router()

@router.message(Command("start"), F.text)
async def start_handler(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id

    if await is_musician_registered(chat_id):
        await message.answer("Ви вже зареєстровані в боті.")
        return

    await message.answer("Вас вітає реєстраційний бот для музикантів! Давайте розпочнемо.")
    await state.update_data(chat_id=chat_id)
    await message.answer("Введіть прізвище. Надішліть 1 якщо хочете використовувати прізвище з телеграм аккаунту")
    await state.set_state(Registration.WaitingForFirstName)


@router.message(Registration.WaitingForFirstName, F.text)
async def process_first_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть коректне ім'я музиканта.")
        return

    await state.update_data(first_name=message.text)
    await message.answer("Введіть ім'я. Правила ті ж самі - надішліть 1 щоб використовувати ім'я з телеграму :")
    await state.set_state(Registration.WaitingForLastName)

@router.message(Registration.WaitingForLastName, F.text)
async def process_last_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть коректне прізвище музиканта.")
        return
    elif str(message.text) == "1":
        await state.update_data(last_name=message.from_user.last_name)
    else:
        await state.update_data(last_name=message.text)
    await message.answer("Ваш вік:")
    await state.set_state(Registration.WaitingForAge)    
    

@router.message(Registration.WaitingForAge)
async def process_age(message: types.Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Добре. А тепер цифрами: ")
        return
    if int(message.text) < 0 or int(message.text) > 99:
        await message.answer("Ви або надто старі, або ще не народились. Спробуйте ще раз! ")
        return

    await state.update_data(age=message.text)
    await message.answer("Введіть ваше місто:")
    await state.set_state(Registration.WaitingForCity)


@router.message(Registration.WaitingForCity)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введіть вашу масть(поки шо одну):")
    await state.set_state(Registration.WaitingForType)

@router.message(Registration.WaitingForType)
async def process_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("Надішліть фото для профілю. Введіть 1 для використання останнього фото профілю телеграм:")
    await state.set_state(Registration.WaitingForPic)

@router.message(Registration.WaitingForPic)
async def process_pic(message: types.Message, state: FSMContext):
    if message.photo:
        file_id = message.photo[0].file_id
        await state.update_data(pic=file_id)
        await state.update_data(pic=file_id)
    elif str(message.text) == "1":
        user_photos = await bot.get_user_profile_photos(message.from_user.id)
        await state.update_data(pic=user_photos.photos[0][0].file_id)
        await message.answer_photo(user_photos.photos[0][0].file_id)
    elif message.document:
        photo = await bot.download(message.document, BytesIO())
        input_photo = BufferedInputFile(photo.getvalue(), message.document.file_name)
        await state.update_data(pic=input_photo)
        await message.answer_photo(input_photo)
        await state.set_state(Registration.WaitingForDemo)
    elif message.text:
        await message.answer("Комісія") 
        return
    await message.answer("Надішліть аудіо вашої гри! Може бути у форматі голосового повідомлення або файлу. Надішліть 1 якщо не бажаєте мати аудіо у свому профілі. Не соромтесь!:")
    await state.set_state(Registration.WaitingForDemo)
    
@router.message(Registration.WaitingForDemo)
async def process_demo(message: types.Message, state: FSMContext):
    if message.voice:
        file_id = message.voice.file_id
        await state.update_data(demo=file_id)
        await message.answer_voice(file_id)
        await state.set_state(Registration.WaitingForDescription)
    elif message.audio:
        file_id = message.audio.file_id
        await state.update_data(demo=file_id)
        await message.answer_audio(file_id)
        await state.set_state(Registration.WaitingForDescription)
    else: 
        await message.answer("Ноти/табулатура не підтримується для поля Демо. Спробуйте ще раз!")
    await message.answer("Останній крок! Надішліть опис свого профілю: ")
    

@router.message(Registration.WaitingForDescription)
async def process_description(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Спробуйте ще раз, бо ніхто не зрозуміє хто ви.")
        return

    data = await state.get_data()
    result = await add_musician(data['chat_id'], 
                                data['first_name'], 
                                data['last_name'], 
                                data['age'], 
                                data['city'], 
                                data['type'],
                                data['pic'],
                                data['demo'], 
                                message.text)
    if result:
        await message.answer(f"Ви успішно зареєстровані як музикант з ID: {result}")
    else:
        await message.answer("Не вдалося зареєструвати музиканта. Будь ласка, спробуйте знову.")
