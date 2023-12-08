'''
Web backend
'''

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional, Annotated

from lib.utils import WSModel, load_json
from lib.datatype import Page, Table
from lib.db_f import get_books, get_authors, get_phouses

_TITLE = "我的閱讀助手"
_WS_MODEL = WSModel()

app = FastAPI()

templates = Jinja2Templates(directory="src/templates")
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/query/{type_}", response_class=JSONResponse)
async def query(type_: Table, cols: str=None, conditions: str=None):
    print(f"{type_=}")
    print(f"{cols=}")
    print(f"{conditions=}")
    prep = lambda s: s if s is None else s.replace('>', '=').split(';')
    data = {
        "books": get_books,
        "authors": get_authors,
        "phouses": get_phouses,
    }[type_](prep(cols), prep(conditions))

    return data

@app.get("/ws", response_class=JSONResponse)
async def search(search_str: str=None):
    print(f"{search_str=}")
    seg_words = None if search_str is None else _WS_MODEL.inference(search_str)

    data = {
        "seg_words": seg_words,
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