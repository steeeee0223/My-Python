import json
from fastapi import FastAPI, File, Request, Form, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

# Import from Files
# REMEMBER TO ADD . BACK
from .utils.util import getId
from .page import createPage
from .database import createDatabase, readDatabase

# Fetch token
file = open('notion-app/SECRET.json')
data = json.load(file)
token = data['token']
headers = data['headers']
headers["Authorization"] = f'Bearer {token}'

app = FastAPI()

# cors
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# template & static files
templates = Jinja2Templates(directory="notion-app/templates")
app.mount("/static", StaticFiles(directory="notion-app/static"), name="static")

@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    print('Running main...')
    return templates.TemplateResponse('index.html', {'request': request})

@app.get('/create/', response_class=HTMLResponse)
async def get_create_page(request: Request):
    print('Running get_create_page...')
    return templates.TemplateResponse('create.html', {'request': request})

@app.post('/create/', response_class=HTMLResponse)
async def create_database(request: Request, page_url: str =Form(), database_name: str =Form()):
    print('Running create_database...')

    page_id = getId(page_url)
    database_id = createDatabase(page_id, database_name)

    redirect_url = request.url_for('get_upload_page', id=database_id)
    print(f'Redirecting to {redirect_url}...')
    return RedirectResponse(redirect_url, status_code=303)

@app.get('/select/', response_class=HTMLResponse)
async def get_select_page(request: Request):
    print('Running get_create_page...')
    return templates.TemplateResponse('select.html', {'request': request})

@app.post('/select/', response_class=HTMLResponse)
async def select_database(request: Request, database_url: str =Form()):
    print('Running select_database...')

    database_id = getId(database_url)
    redirect_url = request.url_for('get_upload_page', id=database_id)

    print(f'Redirecting to {redirect_url}...')
    return RedirectResponse(redirect_url, status_code=303)

@app.get('/upload/{id}', response_class=HTMLResponse)
async def get_upload_page(request: Request, id: str):
    print('Running get_upload_page...')
    return templates.TemplateResponse('upload.html', {'request': request, 'id': id})

@app.post('/upload/{id}', response_class=HTMLResponse)
async def upload_files(request: Request, id: str, file_lists: list[UploadFile]):
    print('Running upload_files...')

    return templates.TemplateResponse(name='upload.html', context={
        'request': request, 'id': id
    })

@app.post('/submit/{id}', response_class=HTMLResponse)
async def submitEachFile(request: Request, id: str, file: UploadFile=File(...)):
    print(f'Running submit... {file.filename}')
    
    code = createPage(id, file)
    match code:
        case 200: return f'{file.filename} PASSED'
        case 415: return f'{file.filename} IGNORED'
        case _: 
            print(f'Result code {code}')
            return f'{file.filename} PAYLOAD TOO LARGE'

# readDatabase("a5236de701154552a04315e398e098c8")