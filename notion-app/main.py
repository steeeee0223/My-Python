import json
import uuid
import asyncio
from fastapi import FastAPI, Request, Form, Response, UploadFile, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Import from Files
# REMEMBER TO ADD . BACK
from .utils.get_id import getId
from .page import createPage
from .database import createDatabase, insertDatabase, readDatabase

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

@app.post('/upload/{id}', response_class=HTMLResponse)
async def upload_files(request: Request, id: str, file_lists: list[UploadFile]):
    print('Running upload_files...')
    result = []
    res = StreamingResponse(insertDatabase(id, file_lists))
    result = [x async for x in res.body_iterator]

    return templates.TemplateResponse(name='upload.html', context={
        'request': request, 'id': id, 'result': result
    })

# work = {'jobs': {}}
# async def do_work(job_key: str, database_id: str, file_lists: list[UploadFile] =[]):
#     for i, file in enumerate(file_lists):
#         code = createPage(database_id, file)
#         jobs = work['jobs']
#         job_info = jobs[job_key]
#         job_info['iteration'] = file.filename
#         job_info['status'] = code
#         await asyncio.sleep(1)
    # work[job_key]['status'] = 'done'

# @app.post('/work/test')
# @app.post('/upload/{id}', response_class=HTMLResponse)
# async def upload_files(request: Request, id: str, files: list[UploadFile]):
#     print('Running upload_files...')
#     identifier = str(uuid.uuid4())
#     work['jobs'][identifier] = {}
#     print(work)
#     asyncio.run_coroutine_threadsafe(do_work(identifier, id, files), loop=asyncio.get_running_loop())

#     return templates.TemplateResponse(name='work.html', context={
#         'request': request, "identifier": identifier
#     })


# @app.get('/work/{id}')
# async def get_testing(request: Request, id: str):
#     identifier = str(uuid.uuid4())
#     work['jobs'][identifier] = {}
#     asyncio.run_coroutine_threadsafe(do_work(identifier, id), loop=asyncio.get_running_loop())

#     return templates.TemplateResponse(name='work.html', context={
#         'request': request, "identifier": identifier
#     })

# @app.get('/status')
# def status(request: Request):
#     return templates.TemplateResponse(name='work.html', context={
#         'request': request, 'all': list(work['jobs'].values()),
#     })

# @app.get('/status/{identifier}')
# async def status_identifier(request: Request, identifier: str):
#     return templates.TemplateResponse(name='work.html', context={
#         'request': request, 
#         "status": work['jobs'].get(identifier, 'job with that identifier is undefined'),
#     })

# readDatabase("a5236de701154552a04315e398e098c8")