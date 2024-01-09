from aiogram.dispatcher.filters.state import State, StatesGroup

class Quiz(StatesGroup):
    category = State()
    mode = State()
    input = State()
    quiz = State()