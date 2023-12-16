from aiogram.fsm.state import StatesGroup, State

class EventRegistration(StatesGroup):
    WaitingForName = State()
    WaitingForDate = State()
    WaitingForLocation = State()
    WaitingForDescription = State()