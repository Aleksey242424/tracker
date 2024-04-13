from src.tracker import tracker as route
from fastapi import Request
from fastapi.responses import RedirectResponse
from jwt import decode
from src.auth.database import Users

@route.get("/tracker/")
async def tracker(request:Request):
    data = request.cookies.get('user')
    if data:
    
        data = decode(data,key="secret",algorithms=["HS256"])
        user = await Users.get_instance(username=data["username"],
                                    password=data["password"])
        return {"data":{
            "username":user.username,
            "password":user.password,
            "email":user.email,
            "is_owner":user.is_owner,
            "worker_type":user.worker_type
        }} 
    return RedirectResponse(url="/auth/login/")