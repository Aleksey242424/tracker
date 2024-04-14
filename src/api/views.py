from src.api import api as router
from fastapi import Query,Request
from fastapi.responses import RedirectResponse
from datetime import datetime,timedelta
from src.auth.database import Users
from src.api.database import UserTimer
from jwt import encode




@router.post("/auth/")
async def login(username:str=Query(),
             password:str|None = Query(default=None),
             position:str=Query(),org_number:int=Query(),
             is_owner:bool=False,
             email:str=Query(default="asdas@mail.ru")):
    user = await Users.get_instance(username=username,password=password)
    token = encode({"username":user.username,"password":user.password},key="secret",algorithm="HS256")
    response = RedirectResponse(f"/api/auth/",status_code=302)
    if user:
        print(user.user_id)
        return response.set_cookie("user",token)
    else:
        await Users.add(username=username,password=password,email=email,is_owner=is_owner,worker_type=position)
        return response.set_cookie("user",token)
    

@router.get("/auth/")
async def login(username:str=Query(),
             password:str|None = Query(default=None),
             position:str=Query(),org_number:int=Query(),
             is_owner:bool=False,
             email:str=Query(default="asdas@mail.ru")):
    user = await Users.get_instance(username=username,password=password)
    
    if user:
        print(user.user_id)
        token = encode({"username":user.username,"password":user.password},key="secret",algorithm="HS256")
        response = RedirectResponse(f"/auth/tracker/",status_code=302)
        response.set_cookie("user",token)
        return {"data":{
            "status":"Login",
            "username":username,
            "password":password,
            "position":position,
            "org_number":org_number
        }}
    else:
        await Users.add(username=username,password=password,email=email,is_owner=is_owner,worker_type=position)
        return {"data":{
            "status":"Register",
            "username":username,
            "password":password,
            "position":position,
            "org_number":org_number
        }}

@router.post("/tracker/add-time/")
async def add_time(request:Request,time:str=Query(),task_id:int=Query(default=1)):
    time = [t for t in time.split(":")]
    import datetime
    time = datetime.time(hour=int(time[0]),minute=int(time[1]),second=int(float(time[2])))
    user = request.cookies.get("user")
    print(time)
    await UserTimer.add(time=time,user_id=2,task_id=1)
    return {"time":time,"task_id":task_id}