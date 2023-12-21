from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    WaitingForType = State()
    WaitingForName = State()
    WaitingForDate = State()
    WaitingForLocation = State()
    WaitingForDescription = State()