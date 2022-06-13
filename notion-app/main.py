import json
from asyncio import sleep
from fastapi import FastAPI, Request, Form, Response, UploadFile, BackgroundTasks, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

# Import from Files
from .utils import getId
from .page import createPage
from .database import createDatabase, insertDatabase

# Fetch token
file = open('notion-app/SECRET.json')
data = json.load(file)
token = data['token']
headers = data['headers']
headers["Authorization"] = f'Bearer {token}'
    

app = FastAPI()

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

async def upload_task(id: str, file: UploadFile, background_tasks: BackgroundTasks):
    background_tasks.add_task(createPage, id, file)
    return background_tasks.tasks[-1]

@app.post('/upload/{id}', response_class=HTMLResponse)
async def upload_files(request: Request, id: str, file_lists: list[UploadFile]):
    print('Running upload_files...')

    failed = insertDatabase(id, file_lists)
        
    return templates.TemplateResponse(name='success.html', context={
        'request': request, 'id': id, 'failed': failed
    })

