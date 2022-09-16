from fastapi import APIRouter, Request, UploadFile
from fastapi.responses import HTMLResponse

from ..dependencies import templates

router = APIRouter(prefix="/upload", tags=["Upload"])


@router.get("/{id}", response_class=HTMLResponse)
async def get_upload_page(request: Request, id: str):
    print("Running get_upload_page...")
    return templates.TemplateResponse("upload.html", {"request": request, "id": id})


@router.post("/{id}", response_class=HTMLResponse)
async def upload_files(request: Request, id: str, file_lists: list[UploadFile]):
    print("Running upload_files...")

    return templates.TemplateResponse(
        name="upload.html", context={"request": request, "id": id}
    )
