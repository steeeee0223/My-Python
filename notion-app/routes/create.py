from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse

from ..dependencies import templates
from ..utils.util import getId
from ..database import createDatabase

router = APIRouter(prefix="/create", tags=["Create"])


@router.get("/", response_class=HTMLResponse)
async def get_create_page(request: Request):
    print("Running get_create_page...")
    return templates.TemplateResponse("create.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def create_database(
    request: Request, page_url: str = Form(), database_name: str = Form()
):
    print("Running create_database...")

    page_id = getId(page_url)
    database_id = createDatabase(page_id, database_name)

    redirect_url = request.url_for("get_upload_page", id=database_id)
    print(f"Redirecting to {redirect_url}...")
    return RedirectResponse(redirect_url, status_code=303)
