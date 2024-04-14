from src.auth import auth as route
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi import Request,Depends,Path,Form,Query
from src.auth.schemes import LoginForm,RegisterForm
from src.auth.database import Users
from src.tracker.database import Company
from jwt import decode,encode




templates = Jinja2Templates(directory="src/auth/templates")

@route.get("/register_company/{user}")
async def register_company(request:Request,user:str=Path(),company_id:str=Query()):
    return templates.TemplateResponse(request=request,name="auth/register_company.html",context={"COMPANY_ID":company_id})
    
@route.post("/register_company/{user}")
async def register_company(request:Request,user:str=Path(),task_name:str=Form()):
    if user:
        user = decode(user,key="secret",algorithms=["HS256"])
        user_obj = await Users.get_instance(username=user["username"],
                                    password=user["password"])
        from random import choice
        from string import ascii_letters
        COMPANY_ID = ''.join(choice(ascii_letters) for i in range(10))
        await Company.add(company_id=COMPANY_ID,owner_id=user_obj.user_id,task_name=task_name)
        return RedirectResponse(f"http://127.0.0.1:8000/auth/register_company/{user}?company_id={COMPANY_ID}",status_code=302)
    

@route.get("/")
@route.get("/login/")
async def login(request:Request):
    return templates.TemplateResponse(request,"auth/login.html")



@route.post("/")
@route.post("/login/")
async def login(data:LoginForm = Depends(LoginForm.as_form)):
    user = await Users.get_instance(username=data.username,password=data.password)
    token = encode({"username":user.username,"password":user.password},key="secret",algorithm="HS256")
    response = RedirectResponse(f"/tracker/{token}",status_code=302)
    response.set_cookie("user",token)
    return response
    
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
    token = encode({"username":user.username,"password":user.password},key="secret",algorithm="HS256")
    response = RedirectResponse(f"/tracker/{token}",status_code=302)
    
    response.set_cookie("user",token)
    return response

