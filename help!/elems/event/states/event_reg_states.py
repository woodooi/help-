from aiogram.fsm.state import StatesGroup, State

class Registration(StatesGroup):
    waitingForType = State()
    WaitingForName = State()
    WaitingForDate = State()
    WaitingForLocation = State()
    WaitingForDescription = State()