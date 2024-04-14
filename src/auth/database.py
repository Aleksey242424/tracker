from src.auth.models import Users as UsersTable,UserTime as UserTimerTable
from sqlalchemy.future import select
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
        
    @staticmethod
    async def get_user_by_company_id(owner_id:int,async_session=get_async_session()):
        async with async_session() as session:
            users_data = await session.execute(select(UsersTable).join(UserTimerTable,UsersTable.user_id==UserTimerTable.user_id).where(UsersTable.user_id == owner_id))
            return users_data.all()
        