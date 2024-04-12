from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import sessionmaker
from database import engine

def get_async_session():
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    return async_session
