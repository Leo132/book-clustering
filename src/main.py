'''
Web backend
'''

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Optional, Annotated

from lib.utils import WSModel
from lib.datatype import Page

_TITLE = "我的閱讀助手"
_WS_MODEL = WSModel()

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


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

    return templates.TemplateResponse(f"index.html", kwargs)

@app.get("/{page}", response_class=HTMLResponse)
async def load_page(request: Request, page: Page, background_tasks: BackgroundTasks):
    print(f"load {page}.html...")
    if page == Page.index:
        print("background processing...")
        background_tasks.add_task(_WS_MODEL.load_model, _WS_MODEL)
    kwargs = {
        "request": request,
        "title": _TITLE,
    }

    return templates.TemplateResponse(f"{page}.html", kwargs)
