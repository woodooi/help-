from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from ...server import add_event
from ..states.event_reg_states import Registration

event_registration_router = Router()

event_options = ["Concert", "Kvartirnik", "Audition", "Rehersal", "Gig", "Recording", "Tutor"]

event_type_opt = [
    [KeyboardButton(text=option) for option in event_options]
]


@event_registration_router.message(Command("event_reg"))
async def start_handler(message: types.Message, state: FSMContext):
    keyboard = ReplyKeyboardMarkup(keyboard=event_type_opt)
    await message.answer("Що ви хочете зареєструвати сьогодні?", reply_markup=keyboard)
    await state.set_state(Registration.WaitingForType)

@event_registration_router.message(Registration.WaitingForType)
async def set_type(message: types.Message, state: FSMContext):
    if message.text not in event_options:
        await message.answer("Тицяйте на кнопку!")
        return
    await state.update_data(event_type=message.text)
    await message.answer("Введіть ім'я", reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
    await state.set_state(Registration.WaitingForName)

@event_registration_router.message(Registration.WaitingForName)
async def set_name(message: types.Message, state: FSMContext):
    await state.update_data(event_name=message.text)
    await message.answer("Введiть дату")
    await state.set_state(Registration.WaitingForDate)


@event_registration_router.message(Registration.WaitingForDate)
async def set_descript(message: types.Message, state: FSMContext):
    await state.update_data(event_date=message.text)
    await message.answer("Введіть локацію ")
    await state.set_state(Registration.WaitingForLocation)


@event_registration_router.message(Registration.WaitingForLocation)
async def set_location(message: types.Message, state: FSMContext):
    await state.update_data(event_location=message.text)
    await message.answer("Введіть опис")
    await state.set_state(Registration.WaitingForDescription)


@event_registration_router.message(Registration.WaitingForDescription)
async def set_date(message: types.Message, state: FSMContext):
    await state.update_data(event_description=message.text)
    data = await state.get_data()
    await state.clear()
    event_to_add = await add_event(data['event_name'], data['event_date'], data['event_location'],
                                   data['event_description'], data['event_type'])
    if event_to_add:
        return await message.answer(f"Подію зареєстровано:{event_to_add}")
    else:
        return await message.answer("сорян")
