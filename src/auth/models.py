from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.types import VARCHAR,INTEGER,BOOLEAN,Time
from database import Base
import enum
from sqlalchemy import func,text
from datetime import datetime,timedelta,time


class WorkerType(enum.Enum):
    null = None
    frontend = "Frontend"
    backend = "Backend"
    fullstack = "FullStack"
    datascience = "Datascience"

class Users(Base):
    __tablename__ = "users"
    user_id:Mapped[int]=mapped_column(INTEGER,primary_key=True)
    username:Mapped[str]=mapped_column(VARCHAR(255))
    password:Mapped[str]=mapped_column(VARCHAR(255),nullable=True)
    email:Mapped[str]=mapped_column(VARCHAR(255),nullable=True)
    is_owner:Mapped[bool]=mapped_column(BOOLEAN)
    company_id:Mapped[int] = mapped_column(VARCHAR(255),nullable=True)
    worker_type:Mapped[WorkerType]=mapped_column(nullable=True)


class UserTime(Base):
    __tablename__ = "user_time"
    user_time_id:Mapped[int] = mapped_column(INTEGER,primary_key=True)
    time:Mapped[datetime] = mapped_column(Time,default=time(hour=0, minute=0, second=0))
    user_id:Mapped[int] = mapped_column(INTEGER,ForeignKey("users.user_id",ondelete="CASCADE",onupdate="CASCADE"))
    task_id:Mapped[int] = mapped_column(INTEGER,ForeignKey("task.task_id",ondelete="CASCADE",onupdate="CASCADE"))

class Task(Base):
    __tablename__ = 'task'
    task_id:Mapped[int] = mapped_column(INTEGER,primary_key=True)
    task_name:Mapped[str] = mapped_column(VARCHAR(255))
    user_id:Mapped[int] = mapped_column(INTEGER,ForeignKey("users.user_id",ondelete="CASCADE",onupdate="CASCADE"))



class Company(Base):
    __tablename__ = "company"
    id:Mapped[int]=mapped_column(INTEGER,primary_key=True)
    task_name:Mapped[str] = mapped_column(VARCHAR(255),nullable=True)
    company_id:Mapped[str]=mapped_column(VARCHAR,unique=True)
    owner_id:Mapped[int] = mapped_column(INTEGER,ForeignKey("users.user_id",ondelete="CASCADE",onupdate="CASCADE"))



