from aiogram.fsm.state import StatesGroup, State


class UserSearch(StatesGroup):
    WaitingForCity = State()
    WaitingForType = State()
