from fastapi import FastAPI

app = FastAPI()


from src.auth import auth
app.include_router(auth)