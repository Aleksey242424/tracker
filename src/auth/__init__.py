from fastapi import APIRouter

auth = APIRouter(prefix="/auth",tags=["Auth"])

from src.auth import views