from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/auth/static", StaticFiles(directory="src/auth/static"), name="static_auth")

from src.auth import auth
from src.api import api
app.include_router(auth)
app.include_router(api)