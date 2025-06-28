from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    location_data = State()
    video = State()
