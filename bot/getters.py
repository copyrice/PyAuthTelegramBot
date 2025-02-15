import time
import pyotp
from aiogram_dialog import DialogManager
from database.models.user import User
from bot.functions import get_user_authentifications_display, get_user_from_dialog_manager_start_data, get_auth_from_dialog_manager_start_data

async def get_auth_background_data(dialog_manager: DialogManager, **kwargs):

    data = {}
    auth = get_auth_from_dialog_manager_start_data(dialog_manager)

    print(auth.key)
    totp = totp = pyotp.TOTP(auth.key)
    current_otp = totp.now()
    time_remaining = totp.interval - (time.time() % totp.interval)

    dialog_manager.dialog_data['progress'] = int(time_remaining)

    data['progress'] = int(time_remaining)
    data['auth_key'] = auth.key
    data['current_otp'] = current_otp

    return data

async def all_authentifications_getter(dialog_manager: DialogManager, **kwargs):
    
    data = {}

    user = get_user_from_dialog_manager_start_data(dialog_manager)

    db_session = dialog_manager.middleware_data.get('db_session')

    authentifications_display = await get_user_authentifications_display(user_id=user.id, session=db_session)

    dialog_manager.dialog_data['authentifications_display'] = authentifications_display

    data['authentifications_display'] = authentifications_display

    return data

async def add_auth_getter(dialog_manager: DialogManager, **kwargs):
    
    data = {}

    name = dialog_manager.dialog_data.get('auth_name')
    auth_key = dialog_manager.dialog_data.get('auth_key')

    add_new_auth_message = f"Name: {name}\nKey: {auth_key}"

    data['add_new_auth_message'] = add_new_auth_message

    return data