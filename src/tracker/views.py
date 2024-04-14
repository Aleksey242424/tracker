from src.tracker import tracker as route
from fastapi import Request,Path
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from jwt import decode
from src.auth.database import Users
from fastapi import WebSocket, WebSocketDisconnect
from src.tracker.database import Company

templates = Jinja2Templates(directory="src/tracker/templates")


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@route.get("/{user}")
async def tracker(request:Request,user:str=Path()):
    data = decode(user,key="secret",algorithms=["HS256"])
    user_obj = await Users.get_instance(username=data["username"],
                                password=data["password"])
    """return {"data":{
            "username":user.username,
            "password":user.password,
            "email":user.email,
            "is_owner":user.is_owner,
            "worker_type":user.worker_type
        }} """
    return templates.TemplateResponse(request=request,name="tracker/tracker_info.html",context={"TOKEN":user})

@route.get("/your_tasks/{user}")
async def tracker(request:Request,user:str=Path()):
    data = decode(user,key="secret",algorithms=["HS256"])
    user_obj = await Users.get_instance(username=data["username"],
                                password=data["password"])
    tasks = await Company.get_all(owner_id=user_obj.user_id)
    print(tasks)
    return templates.TemplateResponse(request=request,name="tracker/your_tasks.html",context={"tasks":tasks,"user":user})


@route.get("/your_tasks/{user}/task/{owner_id}/info/")
async def task(request:Request,owner_id:int=Path()):
    users = await Users.get_user_by_company_id(owner_id=owner_id)
    return templates.TemplateResponse(request=request,name="tracker/all_users_on_task.html",context={"users":users})

@route.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} left the chat")

