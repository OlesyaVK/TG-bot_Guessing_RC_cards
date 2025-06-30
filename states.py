from aiogram.fsm.state import State, StatesGroup

class GameStates(StatesGroup):
    waiting_for_card = State()
    waiting_for_attempts = State()
    waiting_for_answer = State()
    game_in_progress = State()