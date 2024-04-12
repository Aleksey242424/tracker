from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
from os import getenv

class Base(DeclarativeBase):
    pass

load_dotenv()

DB_CONNECT = f'{getenv("DB_DIALECT")}+{getenv("DB_API")}://{getenv("DB_USER")}:{getenv("DB_PASSWORD")}@{getenv("DB_HOST")}:{getenv("DB_PORT")}/{getenv("DB_NAME")}'

engine = create_async_engine(DB_CONNECT)


