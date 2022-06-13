import requests
import json
from fastapi import UploadFile

from .block import writeJson
from .page import createPage
from .schemas.database import Database

# Fetch token
file = open('notion-app/SECRET.json')
data = json.load(file)
token = data['token']
headers = data['headers']
headers["Authorization"] = f'Bearer {token}'

def readDatabase(database_id: str):
    '''Retrieve the database with `database id`'''
    url = f'https://api.notion.com/v1/databases/{database_id}'
    res = requests.get(url=url, headers=headers)
    print(res.status_code)
    data = res.json()
    writeJson('./notion-app/json/db.json', data)

def createDatabase(page_id: str, db_name: str):
    '''
    Sets up a database as a subpage inside an existing page.
    Returns the created `database_id`
    '''
    url = "https://api.notion.com/v1/databases"
    database = Database(page_id, db_name, Name="title", Tags="multi_select", Language="select").__dict__
    res = requests.post(url=url, headers=headers, json=database)
    print(res.status_code)
    res_data = dict(res.json())
    if res.status_code != 200: print(res_data['message']); return
    new_url = res_data['url']
    database_id = new_url.split('/')[-1]
    return database_id

def insertDatabase(database_id: str, file_lists: list[UploadFile]) -> dict[str,list]:
    failed = {'ignored': [], 'content': []}
    for file in file_lists:
        code = createPage(database_id, file)
        if not code: 
            failed['ignored'].append(file.filename); print('/', end='')
        elif code != 200: 
            failed['content'].append(file.filename); print('x', end='')
        else: print('#', end='')
    print('')
    return failed

