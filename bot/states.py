from aiogram.fsm.state import State, StatesGroup

class States(StatesGroup):
    edit = State()
    prorab_add_id = State()
    prorab_remove_id = State()
    prorab_add_name = State()