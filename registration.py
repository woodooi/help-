from aiogram.fsm.state import StatesGroup, State


class Registration(StatesGroup):
    WaitingForID = State()
    WaitingForFirstName = State()
    WaitingForLastName = State()
    WaitingForAge = State()
    WaitingForCity = State()
    WaitingForType = State()
    WaitingForDescription = State()