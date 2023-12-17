from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F

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
    await message.answer("Введіть ім'я музиканта:")
    await state.set_state(Registration.WaitingForFirstName)


@router.message(Registration.WaitingForFirstName, F.text)
async def process_first_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть коректне ім'я музиканта.")
        return

    await state.update_data(first_name=message.text)
    await message.answer("Введіть прізвище музиканта:")
    await state.set_state(Registration.WaitingForLastName)

@router.message(Registration.WaitingForLastName, F.text)
async def process_last_name(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть коректне прізвище музиканта.")
        return

    await state.update_data(last_name=message.text)
    await message.answer("Введіть вік музиканта:")
    await state.set_state(Registration.WaitingForAge)

@router.message(Registration.WaitingForAge)
async def process_age(message: types.Message, state: FSMContext):

    if not message.text.isdigit():
        await message.answer("Будь ласка, введіть коректний вік музиканта (лише цифри).")
        return

    await state.update_data(age=message.text)
    await message.answer("Введіть місто музиканта:")
    await state.set_state(Registration.WaitingForCity)


@router.message(Registration.WaitingForCity)
async def process_city(message: types.Message, state: FSMContext):
    await state.update_data(city=message.text)
    await message.answer("Введіть тип музиканта:")
    await state.set_state(Registration.WaitingForType)

@router.message(Registration.WaitingForType)
async def process_type(message: types.Message, state: FSMContext):
    await state.update_data(type=message.text)
    await message.answer("Введіть опис музиканта:")
    await state.set_state(Registration.WaitingForDescription)

@router.message(Registration.WaitingForDescription)
async def process_description(message: types.Message, state: FSMContext):
    if not message.text or not message.text.strip():
        await message.answer("Будь ласка, введіть коректний опис музиканта.")
        return

    data = await state.get_data()
    result = await add_musician(data['chat_id'], data['first_name'], data['last_name'], data['age'], data['city'],
                                data['type'], message.text)

    if result:
        await message.answer(f"Ви успішно зареєстровані як музикант з ID: {result}")
    else:
        await message.answer("Не вдалося зареєструвати музиканта. Будь ласка, спробуйте знову.")
