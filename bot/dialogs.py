from magic_filter import F
import operator
from aiogram_dialog.widgets.input import MessageInput
from aiogram.types import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const, Multi, Progress
from aiogram_dialog.widgets.kbd import Button, Back
from aiogram_dialog.widgets.kbd import Select, SwitchTo, Group, Cancel, ScrollingGroup, Start
from bot.states import MainMenu, AuthentificationsMenu, SingleAuthentificationMenu, AddAuthentificationMenu
from bot.widgets import SecondsProgress
from bot.onclicks import (on_auth_done_click, on_all_authentifications_start_click, on_auth_choose, on_auth_add_click, on_click, on_done_click,
                          on_add_auth_finalize_click, on_delete_auth_click)
from bot.getters import (get_auth_background_data, all_authentifications_getter, add_auth_getter)
from bot.handlers import (enter_auth_key, add_new_auth_handler, other_type_handler)
from bot.items import scrolling_group_size



back_button = Back(
    Const("<<"),
    id='b_back',
    on_click=on_click
    )

dialogs = [
Dialog(
    Window(
        Const("Authentificator Bot"),
        Button(
            Const('🔐 My authentificatons'),
            id='get_authentications',
            on_click=on_all_authentifications_start_click
        ),
    state=MainMenu.start,
    ),
),
Dialog(
    Window(
        Const('Authentifications'),
        ScrollingGroup(
            Select(
                Format("{item[0]}"),
                items='authentifications_display',
                item_id_getter=operator.itemgetter(2),
                id="auth_item",
                on_click=on_auth_choose,
                ),
                id="auth_select",
                width=scrolling_group_size['width'],
                height=scrolling_group_size['height'],
            ),
            Button(
                    Const("➕ Add auth..."),
                    id='add_auth_button',
                    on_click=on_auth_add_click,
            ),
            Button(
                Const("<<"),
                id='auths_done',
                on_click=on_done_click
            ),
            state=AuthentificationsMenu.all_authentifications,
            parse_mode='HTML',
            getter=all_authentifications_getter
    )
),
Dialog(
    Window(
        Multi(
            Format("Code: <code>{current_otp}</code>\n{auth_key}"),
            SecondsProgress("progress", 30),
        ),
        Button(
            Const("✅"),
            id='auth_done',
            on_click=on_auth_done_click
        ),
        Button(
            Const("❌ Delete auth"),
            id='auth_delete',
            on_click=on_delete_auth_click
        ),
        state=SingleAuthentificationMenu.authentification,
        parse_mode='HTML',
        getter=get_auth_background_data
        )
    ),
Dialog(
    Window(
        Const('Enter name for new authentification...'),
        MessageInput(add_new_auth_handler, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),

        Cancel(
            Const("<<"),
            id='b_cancel'
        ),

        state=AddAuthentificationMenu.enter_name,
        parse_mode='HTML'
    ),
    Window(
        Const('Enter auth key...'),
        MessageInput(enter_auth_key, content_types=[ContentType.TEXT]),
        MessageInput(other_type_handler),

        back_button,

        state=AddAuthentificationMenu.enter_key,
        parse_mode='HTML'
    ),
    Window(
        Format('{add_new_auth_message}'),
        Button(
            Format("✅ Add auth"),
            id='add_auth_finalize',
            on_click=on_add_auth_finalize_click
        ),
        Cancel(
            Format('❌ Cancel'),
            id='cancel_finalize'
        ),

        back_button,

        state=AddAuthentificationMenu.finalize,
        parse_mode='HTML',
        getter=add_auth_getter
    ),
)
]