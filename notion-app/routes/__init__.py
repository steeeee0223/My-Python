from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from ..dependencies import templates
from . import create, select, upload, submit

main_router = APIRouter()
# to register other routes beyond "/"
main_router.include_router(create.router)
main_router.include_router(select.router)
main_router.include_router(upload.router)
main_router.include_router(submit.router)


@main_router.get("/", response_class=HTMLResponse)
async def main(request: Request):
    print("Running main...")
    return templates.TemplateResponse("index.html", {"request": request})
