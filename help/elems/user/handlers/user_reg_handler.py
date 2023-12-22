from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import BufferedInputFile, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from io import BytesIO


from ....bot import bot

from ...server import add_musician, find_self_by_id
from ..states.user_reg_states import UserRegistration

available_types = ["Гітара", "Піаніно", "Скрипка", "Ударні", "Вокал", "Бас-гітара", "Наст. крок"] 
types_to_user = set()

type_keyboard = [
    [KeyboardButton(text=music_type) for music_type in available_types]
]

registration_router = Router()

keyboard_for_reg = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=type_keyboard)

@registration_router.message(Command("registration"), F.text)
async def start_handler(message: types.Message, state: FSMContext):
    chat_id = message.from_user.id
    username = message.from_user.username

    is_registered = await find_self_by_id(chat_id)
    if is_registered is not None:
        await message.answer("Ви вже зареєстровані в боті.")
        return

    await message.answer("Вас вітає реєстраційний бот для музикантів! Давайте розпочнемо.")
    await state.update_data(chat_id=chat_id, username=username)
    await message.answer("Введіть прізвище. Надішліть 1 якщо хочете використовувати прізвище з телеграм аккаунту")
    await state.set_state(UserRegistration.WaitingForFirstName)


@registration_router.message(UserRegistration.WaitingForFirstName, F.text)
async def process_first_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть коректне ім'я музиканта.")
        return
    if message.text == "1":
        await state.update_data(first_name=message.from_user.first_name)
    else:
        await state.update_data(first_name=message.text)
    await message.answer("Введіть ім'я. Правила ті ж самі - надішліть 1 щоб використовувати ім'я з телеграму :")
    await state.set_state(UserRegistration.WaitingForLastName)

@registration_router.message(UserRegistration.WaitingForLastName, F.text)
async def process_last_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть коректне прізвище музиканта.")
        return
    elif message.text == "1":
        await state.update_data(last_name=message.from_user.last_name)
    else:
        await state.update_data(last_name=message.text)
    await message.answer("Ваш вік:")
    await state.set_state(UserRegistration.WaitingForAge)    
    

@registration_router.message(UserRegistration.WaitingForAge)
async def process_age(message: types.Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Добре. А тепер цифрами: ")
        return
    if int(message.text) < 0 or int(message.text) > 99:
        await message.answer("Ви або надто старі, або ще не народились. Спробуйте ще раз! ")
        return

    await state.update_data(age=message.text)
    await message.answer("Введіть ваше місто:")
    await state.set_state(UserRegistration.WaitingForCity)


@registration_router.message(UserRegistration.WaitingForCity)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введіть вашу масть:", reply_markup=keyboard_for_reg)
    await state.set_state(UserRegistration.WaitingForType)

@registration_router.message(UserRegistration.WaitingForType)
async def process_type(message: types.Message, state: FSMContext):
    if message.text not in available_types:
        await message.answer("she raz", reply_markup=keyboard_for_reg)
        return
    elif message.text == "Наст. крок":  
        await state.update_data(type=list(types_to_user))
        await message.answer("Надішліть фото для профілю. Введіть 1 для використання останнього фото профілю телеграм:", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
        await state.set_state(UserRegistration.WaitingForPic)
    else:    
        types_to_user.add(message.text)    

@registration_router.message(UserRegistration.WaitingForPic)
async def process_pic(message: types.Message, state: FSMContext):
    if message.photo:
        await message.answer("1")
        file_id = message.photo[0].file_id
        await state.update_data(pic=file_id)
    elif str(message.text) == "1":
        user_photos = await bot.get_user_profile_photos(message.from_user.id)
        await state.update_data(pic=user_photos.photos[0][0].file_id)
    elif message.document:
        await message.answer("2")
        photo = await bot.download(message.document, BytesIO())
        input_photo = BufferedInputFile(photo.getvalue(), message.document.file_name)
        await state.update_data(pic=input_photo)
        await state.set_state(UserRegistration.WaitingForDemo)
    elif message.text:
        await message.answer("Комісія") 
        return
    await message.answer("Надішліть аудіо вашої гри! Може бути у форматі голосового повідомлення або файлу. Надішліть 1 якщо не бажаєте мати аудіо у свому профілі. Не соромтесь!:")
    await state.set_state(UserRegistration.WaitingForDemo)
    
@registration_router.message(UserRegistration.WaitingForDemo)
async def process_demo(message: types.Message, state: FSMContext):
    if message.text == "1":
        await state.set_state(UserRegistration.WaitingForDescription)
        await state.update_data(demo="")
    elif message.voice:
        file_id = message.voice.file_id
        await state.update_data(demo=file_id)
        await state.set_state(UserRegistration.WaitingForDescription)
    elif message.audio:
        file_id = message.audio.file_id
        await state.update_data(demo=file_id)
    else: 
        await message.answer("Не чує баба! Спробуйте ще раз!")
        return
    await message.answer("Останній крок! Надішліть опис свого профілю: ")
    

@registration_router.message(UserRegistration.WaitingForDescription)
async def process_description(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Спробуйте ще раз, бо ніхто не зрозуміє хто ви.")
        return

    data = await state.get_data()
    print(data)
    result = await add_musician(data['chat_id'], 
                                data['username'],
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
    await state.clear()
