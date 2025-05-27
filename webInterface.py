import uvicorn
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import main

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def mainpage(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})

@app.post("/analyze")
async def analyze(request: Request):
    data = await request.json()

    calc_coef = data['mode']['calc_coef']
    predict_result = data['mode']['predict_result']
    print(predict_result)

    coef = []
    result = None
    if calc_coef:
        coef = main.calc_coef(data)
        data['coefficients'] = coef
    if predict_result:
        result = main.predict_result(data)

    print({"coef": coef, "result": result})
    return {"coef": coef, "result": result}


if __name__ == "__main__":
    uvicorn.run("webInterface:app", reload=True)