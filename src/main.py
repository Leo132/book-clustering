'''
Main application
'''

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

_TITLE = "我的閱讀助手"

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/{page}", response_class=HTMLResponse)
async def load_page(request: Request, page: str):
    print(f"load {page}.html...")
    kwargs = {
        "request": request,
        "title": _TITLE,
    }
    return templates.TemplateResponse(f"{page}.html", kwargs)
