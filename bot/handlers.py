
from aiogram.types import Message
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import DialogManager
from bot.states import AddAuthentificationMenu
from bot.functions import is_valid_totp_secret
async def other_type_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
):
    await message.answer("Unknwon input")



async def add_new_auth_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager
    ):
     
    auth_name = message.text

    if(auth_name):
        dialog_manager.dialog_data['auth_name'] = auth_name
        await dialog_manager.switch_to(AddAuthentificationMenu.enter_key)
    
    else:
        await message.answer("Error, enter correct name")
        return


async def enter_auth_key(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager
    ):
     
    auth_key = message.text

    if(auth_key):

        if(is_valid_totp_secret(auth_key)):

            dialog_manager.dialog_data['auth_key'] = auth_key
            await dialog_manager.switch_to(AddAuthentificationMenu.finalize)
    
        else:
            await message.answer("Error, enter correct auth key")
            return
    else:
        return