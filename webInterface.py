import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def mainpage(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()
    print(data)
    return 200


if __name__ == "__main__":
    uvicorn.run("webInterface:app", reload=True)