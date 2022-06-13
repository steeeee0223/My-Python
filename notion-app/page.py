import json
import requests
from fastapi import UploadFile
from pathlib import PurePath

from .schemas.setting import languages
from .schemas.block import CodeBlock
from .schemas.page import Page
from .block import writeJson

# Fetch token
file = open('notion-app/SECRET.json')
data = json.load(file)
token = data['token']
headers = data['headers']
headers["Authorization"] = f'Bearer {token}'

# Ignore files and folders
ignore = {'.DS_Store', 'Icon\r', 
          '.vscode', '.ipynb_checkpoints', '__pycache__', '.git', 
          '.devcontainer'}

def createPage(database_id: str, file: UploadFile) -> int|None:
    url = f'https://api.notion.com/v1/pages'
    path = file.filename
    obj = PurePath(path)
    tags = obj.parts
    if ignore.intersection(tags): return # path
    name, ext = obj.stem, obj.suffix
    if ext not in languages: return # path
    language = languages[ext]

    content = file.file.read().decode('utf8')
    block = CodeBlock(content, language).__dict__
    page = Page(database_id, name, language, 'Active', *tags[:-1], block=block)
    res = requests.post(url=url, headers=headers, json=page.__dict__)
    code = res.status_code
    return code

def retrievePage(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    res = requests.get(url, headers=headers)
    print(res.status_code)
    data = res.json()
    writeJson('./notion-app/json/page1.json', data)


