from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from db import add_musician
from registration import Registration

router = Router()


@router.message(Command("start"))
async def start_handler(message: types.Message, state: FSMContext):
    await message.answer("Вас вітає реєстраційний бот для музикантів! Давайте розпочнемо.")
    await message.answer("Введіть ID музиканта:")
    await state.set_state(Registration.WaitingForID)

@router.message(Registration.WaitingForID)
async def process_id(message: types.Message, state: FSMContext):
    await state.update_data(musician_id=message.text)
    await message.answer("Введіть ім'я музиканта:")
    await state.set_state(Registration.WaitingForFirstName)

@router.message(Registration.WaitingForFirstName)
async def process_first_name(message: types.Message, state: FSMContext):
    await state.update_data(first_name=message.text)
    await message.answer("Введіть прізвище музиканта:")
    await state.set_state(Registration.WaitingForLastName)

@router.message(Registration.WaitingForLastName)
async def process_last_name(message: types.Message, state: FSMContext):
    await state.update_data(last_name=message.text)
    await message.answer("Введіть вік музиканта:")
    await state.set_state(Registration.WaitingForAge)

@router.message(Registration.WaitingForAge)
async def process_age(message: types.Message, state: FSMContext):
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
    data = await state.get_data()
    print(data)
    result = await add_musician(data['musician_id'], data['first_name'], data['last_name'], data['age'], data['city'],
                                data['type'], message.text)
    if result:
        await message.answer(f"Ви успішно зареєстровані як музикант з ID: {result}")
    else:
        await message.answer("Не вдалося зареєструвати музиканта. Будь ласка, спробуйте знову.")

