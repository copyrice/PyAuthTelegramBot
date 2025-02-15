from aiogram import Dispatcher
from aiogram.types import Message
from database.database import db_register_user
from aiogram_dialog import DialogManager, StartMode
from bot.states import MainMenu
from aiogram.filters import CommandStart, Command

def register_commands(dp: Dispatcher):
    dp.message.register(start, CommandStart())

async def start(message: Message, dialog_manager: DialogManager):
    db_session = dialog_manager.middleware_data.get('db_session')
    await db_register_user(session=db_session, username=message.from_user.username, fullname=message.from_user.full_name, user_tg_id=message.from_user.id)
    await dialog_manager.start(MainMenu.start, mode=StartMode.RESET_STACK)