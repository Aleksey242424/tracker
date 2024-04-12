from src.auth import auth as route
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request,Depends
from src.auth.schemes import LoginForm,RegisterForm
from src.auth.user import Users
from jwt import decode,encode

templates = Jinja2Templates(directory="src/auth/templates")

@route.get("/")
@route.get("/login/")
async def login(request:Request):
    return templates.TemplateResponse(request,"auth/login.html")



@route.post("/")
@route.post("/login/")
async def login(data:LoginForm = Depends(LoginForm.as_form)):
    user = await Users.get_instance(username=data.username,password=data.password)
    return {"data":{
        "username":user.username,
        "password":user.password
    }}

@route.get("/register/")
async def register(request:Request):
    return templates.TemplateResponse(request,"auth/register.html")


@route.post("/register/")
async def register_p(data:RegisterForm=Depends(RegisterForm.as_form)):
    await Users.add(username=data.username,
                    password=data.password,
                    email=data.email,
                    is_owner=data.is_owner,
                    worker_type=data.worker_type)
    user = await Users.get_instance(username=data.username,
                                    password=data.password)
    response = RedirectResponse("/auth/tracker/",status_code=302)
    token = encode({"username":user.username,"password":user.password},key="secret",algorithm="HS256")
    response.set_cookie("user",token)
    return response

@route.get("/tracker/")
async def tracker(request:Request):
    data = request.cookies.get('user')
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
@route.post("/tracker/")
async def tracker_p():
    pass