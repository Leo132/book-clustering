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


@app.get("/search", response_class=JSONResponse)
async def search(search_str: str=None, categories: str=None):
    categories = categories.split(';')
    print(f"{search_str=}")
    print(f"{categories=}")
    seg_words = None if search_str is None else _WS_MODEL.inference(search_str)
    print(f"{seg_words=}")
    # query
    result = None

    data = {
        "seg_words": seg_words,
        "categories": categories,
        "result": result,
    }

    return JSONResponse(data)

@app.get("/data/{file}", response_class=JSONResponse)
async def response_data(file: str):
    data = load_json(f"./data/{file}")
    print(f"sending {file}...")
    return JSONResponse(content=data)

@app.get("/data/{folder}/{file}", response_class=JSONResponse)
async def response_data(folder: str, file: str):
    data = load_json(f"./data/{folder}/{file}")
    print(f"sending {file}...")
    return JSONResponse(content=data)

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

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="localhost",
        port=8000,
        reload=True
    )