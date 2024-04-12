from src.auth.models import Users as UsersTable
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from src.auth.utils import get_async_session


class Users:
    @staticmethod
    async def add(username,password,email,is_owner,worker_type=None,async_session=get_async_session()):
        async with async_session() as session:
            session.add(UsersTable(
                                username=username,
                                password=password,
                                email=email,
                                is_owner=is_owner,
                                worker_type=worker_type
                                ))
            await session.commit()

    @staticmethod
    async def get_instance(username,password,async_session=get_async_session()):
        async with async_session() as session:
            instance = await session.execute(select(UsersTable).where(UsersTable.username==username,UsersTable.password==password))
            instance = instance.scalar()
            return instance