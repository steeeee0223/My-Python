from fastapi import APIRouter, Request, UploadFile, File
from fastapi.responses import HTMLResponse

from ..page import createPage

router = APIRouter(prefix="/submit", tags=["Submit"])


@router.post("/{id}", response_class=HTMLResponse)
async def submitEachFile(request: Request, id: str, file: UploadFile = File(...)):
    print(f"Running submit... {file.filename}")

    code = createPage(id, file)
    match code:
        case 200:
            return f"{file.filename} PASSED"
        case 415:
            return f"{file.filename} IGNORED"
        case _:
            print(f"Result code {code}")
            return f"{file.filename} FAILED"
