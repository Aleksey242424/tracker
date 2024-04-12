from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.types import VARCHAR,INTEGER,BOOLEAN
from database import Base

class Users(Base):
    __tablename__ = "users"
    user_id:Mapped[int]=mapped_column(INTEGER,primary_key=True)
    username:Mapped[str]=mapped_column(VARCHAR(255))
    password:Mapped[str]=mapped_column(VARCHAR(255))
    is_owner:Mapped[bool]=mapped_column(BOOLEAN)

class Company(Base):
    __tablename__ = "company"
    id:Mapped[int]=mapped_column(INTEGER,primary_key=True)
    company_id:Mapped[str]=mapped_column(VARCHAR,unique=True)
    user_id:Mapped[int]=mapped_column(INTEGER,ForeignKey(
        "users.user_id",
        ondelete="CASCADE",
        onupdate="CASCADE")
        )


