from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from ..dependencies import templates
from ..utils.util import getId

router = APIRouter(prefix="/select", tags=["Select"])


@router.get("/", response_class=HTMLResponse)
async def get_select_page(request: Request):
    print("Running get_create_page...")
    return templates.TemplateResponse("select.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def select_database(request: Request, database_url: str = Form()):
    print("Running select_database...")

    database_id = getId(database_url)
    redirect_url = request.url_for("get_upload_page", id=database_id)

    print(f"Redirecting to {redirect_url}...")
    return RedirectResponse(redirect_url, status_code=303)
