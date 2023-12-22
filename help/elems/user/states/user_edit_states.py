from aiogram.fsm.state import StatesGroup, State

class UserEdit(StatesGroup):
    WaitingForQuery = State()
    WaitingForTarget = State()