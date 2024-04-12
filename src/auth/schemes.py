from pydantic import BaseModel
from fastapi import Form


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
    is_owner:bool

    @classmethod
    def as_form(cls,
            username:str=Form(),
            password:str=Form(),
            email:str=Form(),
            is_owner:bool=Form()):
        return cls(username=username,
                   password=password,
                   email=email,
                   is_owner=is_owner)