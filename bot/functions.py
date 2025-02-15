import time
import asyncio
import pyotp
from aiogram_dialog import BaseDialogManager, DialogManager
from database.models.auth import Auth
from database.models.user import User
from database.database import db_get_user_authentifications
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Any
from bot.events import auth_user_events
import base64


def get_user_from_dialog_manager_start_data(dialog_manager: DialogManager) -> User:
    return dialog_manager.start_data.get('user')

def get_authentifications_display_from_dialog_manager(dialog_manager: DialogManager) -> list[tuple[str, Auth, int]]:
    return dialog_manager.dialog_data.get('authentifications_display')

def get_tg_user_id_from_dialog_manager(dialog_manager: DialogManager) -> int:
    return dialog_manager.dialog_data.get('tg_user_id')

def get_auth_from_dialog_manager_start_data(dialog_manager: DialogManager) -> Auth:
    return dialog_manager.start_data.get('auth')

def auth_event_is_set(tg_user_id: int):
    global auth_user_events
    event = auth_user_events.get(tg_user_id)
    return event.is_set()

def set_user_event(tg_user_id: int):
    global auth_user_events
    auth_user_events[tg_user_id].set()

def new_user_event(tg_user_id: int):
    global auth_user_events
    auth_user_events[tg_user_id] = asyncio.Event()


def is_valid_totp_secret(secret: str) -> bool:
    try:
        # Проверяем, можно ли декодировать строку как Base32
        base64.b32decode(secret, casefold=True)  # casefold=True позволяет использовать строчные буквы
        
        # Дополнительно проверяем, создаёт ли этот секрет рабочий TOTP
        totp = pyotp.TOTP(secret)
        totp.now()  # Пробуем сгенерировать код — если не выйдет, секрет недействителен
        
        return True
    except (base64.binascii.Error, ValueError):
        return False  # Если декодирование или генерация TOTP не удалась

async def auth_background(dialog_manager: BaseDialogManager, auth_key: str, tg_user_id: int):
    while True:
        await asyncio.sleep(1)
        if auth_event_is_set(tg_user_id=tg_user_id):
            await dialog_manager.done()
            break
        # Ожидание до истечения текущего кода
        totp = pyotp.TOTP(auth_key)
        current_otp = totp.now()
        time_remaining = totp.interval - (time.time() % totp.interval)

        await dialog_manager.update({
            "current_otp": current_otp,
            "progress": int(time_remaining)
        })

async def get_user_authentifications_display(user_id: int, session: AsyncSession) -> list[tuple[str, Auth, int]]:
    
    user_authentifications = await db_get_user_authentifications(session=session, user_id=user_id)

    authentifications_display = [(auth.name, auth, user_authentifications.index(auth)) for auth in user_authentifications]

    return authentifications_display


def find_elem_in_elems_display_by_item_id(elems_display: list[tuple[str, Any, int]], item_id: int) -> Any:
    for pair in elems_display:
        if(pair[2]==int(item_id)):
            elem = pair[1]
            return elem
    return None

