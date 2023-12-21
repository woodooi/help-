from aiogram.fsm.state import StatesGroup, State


class Search(StatesGroup):
    WaitingForCity = State()
    WaitingForType = State()
