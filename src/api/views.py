from src.api import api as router
from fastapi import Query
from datetime import datetime
from src.auth.database import Users

@router.post("/auth/register/")
def register(username:str=Query(),
             password:str|None = Query(default=None),
             position:str=Query(),org_number:int=Query(),
             is_owner:bool=False):
    return {"data":{
        "username":username,
        "password":password,
        "worker_type":position,
        "company_id":org_number,
        "is_owner":is_owner
    }}

@router.post("/auth/")
async def login(username:str=Query(),
             password:str|None = Query(default=None),
             position:str=Query(),org_number:int=Query(),
             is_owner:bool=False,
             email:str=Query(default="asdas@mail.ru")):
    user = await Users.get_instance(username=username,password=password)
    if user:
        return {"data":{
            "status":"Login",
            "username":username,
            "password":password,
            "position":position,
            "org_number":org_number
        }}
    else:
        print("sadsdsads")
        await Users.add(username=username,password=password,email=email,is_owner=is_owner,worker_type=position)
        return {"data":{
            "status":"Register",
            "username":username,
            "password":password,
            "position":position,
            "org_number":org_number
        }}

@router.post("/tracker/add-time/")
def add_time(time:str=Query(),task_id:int=Query(default=1)):
    return {"time":time,"task_id":task_id}