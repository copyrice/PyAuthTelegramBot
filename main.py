import asyncio
from bot.config import BOT_TOKEN, DB_PATH

from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage, SimpleEventIsolation

from aiogram import Router, Bot, Dispatcher
from aiogram.types import Message

from aiogram_dialog import setup_dialogs, DialogManager, StartMode

from bot.dialogs import dialogs
from bot.states import MainMenu

from bot.middlewares.db import DbSessionMiddleware


from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from database.models.base import Base

from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from bot.error_handlers import register_error_handlers
from aiogram.filters import CommandStart, ExceptionTypeFilter

from bot.commands import register_commands

router = Router()
storage = MemoryStorage()





async def db_main(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def main():
    bot = Bot(token=BOT_TOKEN, disable_web_page_preview=True)
    engine = create_async_engine(url=DB_PATH, echo=True)
    await db_main(engine)
    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    dp = Dispatcher(storage=storage)

    for dialog in dialogs:
        dp.include_router(dialog)

    dp.update.middleware(DbSessionMiddleware(session_pool=sessionmaker))

    register_commands(dp)
    register_error_handlers(dp)
    
    
    dp.include_router(router)
    
    setup_dialogs(dp)

    await dp.start_polling(bot)
    # await asyncio.gather(
    #     dp.start_polling(bot)
    # )


asyncio.run(main())
