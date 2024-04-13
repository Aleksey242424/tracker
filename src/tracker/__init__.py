from fastapi import APIRouter
tracker = APIRouter(prefix="/tracker/",tags=["Tracker"])
from src.tracker import views