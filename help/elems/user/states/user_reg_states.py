from aiogram.fsm.state import StatesGroup, State


class UserRegistration(StatesGroup):
    WaitingForID = State()
    WaitingForFirstName = State()
    WaitingForLastName = State()
    WaitingForAge = State()
    WaitingForCity = State()
    WaitingForType = State()
    WaitingForPic = State()
    WaitingForDescription = State()
    WaitingForDemo = State()