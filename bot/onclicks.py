from aiogram_dialog import DialogManager
from aiogram.types import CallbackQuery
from aiogram_dialog.widgets.kbd import Button
from bot.functions import set_user_event, get_user_from_dialog_manager_start_data
from database.database import db_get_user_by_tg_id, db_add, db_delete
from bot.states import AuthentificationsMenu, SingleAuthentificationMenu, AddAuthentificationMenu
from typing import Any
from bot.functions import (find_elem_in_elems_display_by_item_id, get_user_authentifications_display, get_authentifications_display_from_dialog_manager, new_user_event,
                            auth_background, get_tg_user_id_from_dialog_manager, get_auth_from_dialog_manager_start_data)
from database.models.user import User
from database.models.auth import Auth
import asyncio

async def on_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    pass


async def on_done_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.done()


async def on_auth_done_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    tg_user_id = dialog_manager.start_data.get('tg_user_id')
    set_user_event(tg_user_id)


async def on_all_authentifications_start_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    db_session = dialog_manager.middleware_data.get('db_session')
    user = await db_get_user_by_tg_id(session=db_session, tg_id=callback.from_user.id)
    data = {
        'user': user
    }
    await dialog_manager.start(state=AuthentificationsMenu.all_authentifications, data=data)


async def on_auth_add_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    await dialog_manager.start(state=AddAuthentificationMenu.enter_name, data=dialog_manager.start_data)



async def on_auth_choose(
        callback: CallbackQuery,
        widget: Any, dialog_manager: DialogManager,
        item_id: str
):
    authentifications_display = get_authentifications_display_from_dialog_manager(dialog_manager)
    auth: Auth = find_elem_in_elems_display_by_item_id(elems_display=authentifications_display, item_id=int(item_id))
    tg_user_id = get_tg_user_id_from_dialog_manager(dialog_manager)
    new_user_event(tg_user_id)
    start_data = {
        'tg_user_id': tg_user_id,
        'auth': auth
    }
    await dialog_manager.start(state=SingleAuthentificationMenu.authentification, data=start_data)
    asyncio.create_task(auth_background(dialog_manager=dialog_manager.bg(), auth_key=auth.key, tg_user_id=tg_user_id))



async def on_add_auth_finalize_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    db_session = dialog_manager.middleware_data.get('db_session')
    user = get_user_from_dialog_manager_start_data(dialog_manager)

    name = dialog_manager.dialog_data.get('auth_name')
    auth_key = dialog_manager.dialog_data.get('auth_key')

    await db_add(session=db_session, entity=Auth(name=name, key=auth_key, user_id=user.id))
    await dialog_manager.done()


async def on_delete_auth_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
):
    db_session = dialog_manager.middleware_data.get('db_session')
    auth = get_auth_from_dialog_manager_start_data(dialog_manager)

    await db_delete(session=db_session, entity=auth)
    tg_user_id = dialog_manager.start_data.get('tg_user_id')
    set_user_event(tg_user_id)
    # await dialog_manager.done()
    