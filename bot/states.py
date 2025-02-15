from aiogram.fsm.state import State, StatesGroup


class MainMenu(StatesGroup):
    start = State()

class AuthentificationsMenu(StatesGroup):
    all_authentifications = State()
    
class SingleAuthentificationMenu(StatesGroup):
    authentification = State()

class AddAuthentificationMenu(StatesGroup):
    enter_name = State()
    enter_key = State()
    finalize = State()
