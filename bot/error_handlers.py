from bot.states import MainMenu
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram import Dispatcher
from aiogram.filters import CommandStart, ExceptionTypeFilter

from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

def register_error_handlers(dp: Dispatcher):
    dp.errors.register(
        reset_stack_start,
        ExceptionTypeFilter(UnknownIntent),
    )
    dp.errors.register(
        reset_stack_start,
        ExceptionTypeFilter(UnknownState),
    )

async def reset_stack_start(event, dialog_manager: DialogManager):
    # Example of handling UnknownIntent Error and starting new dialog.
    await dialog_manager.start(
        MainMenu.start, mode=StartMode.RESET_STACK
    )
