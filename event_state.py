from aiogram.fsm.state import StatesGroup, State


class EventCreation(StatesGroup):
    WaitingForEventName = State()
    WaitingForEventDescription = State()
    WaitingForEventDate = State()