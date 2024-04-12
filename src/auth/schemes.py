from pydantic import BaseModel
from fastapi import Form
from src.auth.models import WorkerType


class LoginForm(BaseModel):
    username:str
    password:str

    @classmethod
    def as_form(cls,
            username:str=Form(),
            password:str=Form()):
        return cls(username=username,
                   password=password)

class RegisterForm(BaseModel):
    username:str
    password:str
    email:str
    is_owner:bool = True
    worker_type:WorkerType = None
    @classmethod
    def as_form(cls,
            username:str=Form(),
            password:str=Form(),
            email:str=Form()):
        return cls(username=username,
                   password=password,
                   email=email)

