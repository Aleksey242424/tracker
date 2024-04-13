from src.auth.models import Task as TaskTable
from sqlalchemy.future import select
from src.auth.utils import get_async_session

class Task:
    @staticmethod
    async def add(task_name,user_id,async_session=get_async_session()):
        async with async_session() as session:
            session.add(TaskTable(task_name=task_name,user_id=user_id))
            session.commit()

    @staticmethod
    async def get_all(user_id,async_session=get_async_session()):
        async with async_session() as session:
            task = await session.execute(select(TaskTable).where(TaskTable.user_id==user_id))
            return task.all()

    @staticmethod
    async def get(task_id,async_session=get_async_session()):
        async with async_session() as session:
            task = await session.execute(select(TaskTable).where(TaskTable.task_id==task_id))
            return task.scalar()
            