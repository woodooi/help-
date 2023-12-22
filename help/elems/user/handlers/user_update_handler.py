from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from ..states.update_states import UpdateMusicians
from ...server import update_musician

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

update_musicians = Router()


@update_musicians.message(Command('update_musicians'))
async def update_musicians_handler(message: types.Message):
    keyboard_buttons = []

    for field in ["first_name", "last_name", "age", "city", "type", "description"]:
        button_text = field.replace("_", " ").capitalize()
        callback_data = f"update_{field}"
        keyboard_buttons.append(InlineKeyboardButton(text=button_text, callback_data=callback_data))

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        keyboard_buttons[:3],
        keyboard_buttons[3:],
    ])
    await message.answer("Оберіть параметр для оновлення:", reply_markup=keyboard)


@update_musicians.callback_query()
async def process_update_data(callback_query: types.CallbackQuery, state: FSMContext):
    field = callback_query.data.replace("update_", "")

    await callback_query.answer(f"Ви обрали {field} для оновлення. Введіть нове значення:")

    await state.update_data(update_field=field)

    await state.set_state(UpdateMusicians.WaitingForNewValue)


@update_musicians.message(UpdateMusicians.WaitingForNewValue)
async def process_new_value(message: types.Message, state: FSMContext):
    await state.update_data(chat_id=message.from_user.id)
    new_value = message.text
    data = await state.get_data()
    chat_id = data.get("chat_id")
    update_field = data.get("update_field")

    success = await update_musician(chat_id, update_field, new_value)

    if success:
        await message.answer(f"Дані оновлено. {update_field} тепер має значення: {new_value}")
    else:
        await message.answer("Помилка при оновленні даних. Можливо, ви не зареєстровані.")

    await state.clear()


