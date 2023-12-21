from aiogram.fsm.state import StatesGroup, State


class EventSearch(StatesGroup):
    WaitingForCity = State()
    WaitingForType = State()
