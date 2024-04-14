from src.auth.models import UserTime as UserTimeTable
from sqlalchemy.future import select
from src.auth.utils import get_async_session

class UserTimer:
    @staticmethod
    async def add(time,user_id,task_id,async_session=get_async_session()):
        async with async_session() as session:
            session.add(UserTimeTable(time=time,user_id=user_id,task_id=task_id))
            await session.commit()

    @staticmethod
    async def get(user_id,async_session=get_async_session()):
        async with async_session() as session:
            time = await session.execute(select(UserTimeTable).where(UserTimeTable.user_id==user_id))
            return time.scalar()