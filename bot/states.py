from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    choose_date = State()

class CalendarStates(StatesGroup):
    month = State()
    year = State()