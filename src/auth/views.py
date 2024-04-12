from src.auth import auth as route
from fastapi.templating import Jinja2Templates
from fastapi import Request,Depends
from src.auth.schemes import LoginForm

templates = Jinja2Templates(directory="src/auth/templates")

@route.get("/")
@route.get("/login/")
def login(request:Request):
    return templates.TemplateResponse(request,"auth/login.html")



@route.post("/")
@route.post("/login/")
def login(data:LoginForm = Depends(LoginForm.as_form)):
    return {"data":{
        "username":data.username,
        "password":data.password
    }}

@route.get("/register/")
def register(request:Request):
    return templates.TemplateResponse(request,"auth/register.html")


@route.post("/register/")
def register_p():
    return {"message":"register_post"}