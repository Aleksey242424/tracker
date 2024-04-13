from fastapi import APIRouter

api = APIRouter(prefix="/api",tags=["API"])

from src.api import views