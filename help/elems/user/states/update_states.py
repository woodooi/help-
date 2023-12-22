from aiogram.fsm.state import StatesGroup, State


class UpdateMusicians(StatesGroup):
    WaitingForNewValue = State()
