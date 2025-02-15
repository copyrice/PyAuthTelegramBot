from sqlalchemy.exc import IntegrityError
from database.models.user import User
from database.models.auth import Auth
from database.models.base import Base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime


async def db_add(session: AsyncSession, entity: Base):
    session.add(entity) 
    await session.commit()
    await session.refresh(entity)

async def db_delete(session: AsyncSession, entity: Base):
    await session.delete(entity) 
    await session.commit()


async def db_get_user_by_tg_id(session:AsyncSession, tg_id: int):
    sql = select(User).where(User.tg_id==tg_id)
    user_sql = await session.execute(sql)
    return user_sql.scalar()

async def db_register_user(user_tg_id: int, username: str, fullname: str, session:AsyncSession):
    existing_user = await db_get_user_by_tg_id(session=session, tg_id=user_tg_id)
    if existing_user:
        return
    username = username if username else 'username'

    name = fullname if fullname else 'name'
    
    user = User(tg_id=int(user_tg_id), username=username, name=name)
    
    session.add(user)
    
    try:
        await session.commit()
        await session.refresh(user)
        return True
    except IntegrityError:
        await session.rollback()
        return False
    
async def db_get_user_authentifications(session: AsyncSession, user_id: int) -> list[Auth]:
    sql = select(Auth).where(Auth.user_id==user_id)
    result = await session.execute(sql)
    return list(result.scalars())

async def db_get_user_authentifications(session: AsyncSession, user_id: int) -> list[Auth]:
    sql = select(Auth).where(Auth.user_id==user_id)
    result = await session.execute(sql)
    return list(result.scalars())