'''
Web backend
'''

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional, Annotated

from lib.utils import WSModel, load_json
from lib.datatype import Page

_TITLE = "我的閱讀助手"
_WS_MODEL = WSModel()

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/index", response_class=HTMLResponse)
async def main(request: Request, background_tasks: BackgroundTasks, search_str: str=None):
    print("load index.html...")
    print("background processing...")
    background_tasks.add_task(_WS_MODEL.load_model)
    print(f"{search_str=}")
    result = None if search_str is None else _WS_MODEL.inference(search_str)
    print(f"{result=}")
    kwargs = {
        "request": request,
        "title": _TITLE,
        "result": result,
    }

    return templates.TemplateResponse("index.html", kwargs)

@app.get("/{page}", response_class=HTMLResponse)
async def load_page(request: Request, page: Page, background_tasks: BackgroundTasks):
    print(f"load {page}.html...")
    if page == Page.index:
        print("background processing...")
        background_tasks.add_task(_WS_MODEL.load_model)
    kwargs = {
        "request": request,
        "title": _TITLE,
    }

    return templates.TemplateResponse(f"{page}.html", kwargs)

@app.get("/data/{file}", response_class=JSONResponse)
async def response_data(file: str):
    data = load_json(f"./data/{file}")
    print(f"sending {file}...")
    return JSONResponse(content=data)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )