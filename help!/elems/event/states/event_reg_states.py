from aiogram.fsm.state import StatesGroup, State

class EventRegistration(StatesGroup):
    waitingForType = State()
    WaitingForName = State()
    WaitingForDate = State()
    WaitingForLocation = State()
    WaitingForDescription = State()