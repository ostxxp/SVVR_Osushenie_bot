from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    choose_date = State()
    fill_volume = State()
    fill_installers = State()
    wait_for_filter = State()
    wait_for_feedback = State()
