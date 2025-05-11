import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
def mainpage():
    return templates.TemplateResponse("index.html")


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)