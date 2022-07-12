import json
from pprint import pprint
import re
import requests
from fastapi import UploadFile
from pathlib import PurePath

from .schemas.setting import languages
from .schemas.block import CodeBlock
from .schemas.page import Page
from .block import writeJson
from .notebook import createNotebook

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

def splitContent(s: str, n: int=2000):
    def _f(s, n):
        while s: yield s[:n]; s = s[n:]
    return list(_f(s, n))

def createPage(database_id: str, file: UploadFile) -> int|None:
    url = f'https://api.notion.com/v1/pages'
    path = file.filename

    print(f'Uploading file ... {path}')

    obj = PurePath(path)
    tags = obj.parts
    if ignore.intersection(tags): return # path
    name, ext = obj.stem, obj.suffix

    if ext not in languages: return # path
    else:
        language = languages[ext]
        content = file.file.read().decode('utf8')
        if ext == '.ipynb':
            blocks = {
                f'block{i}': block
                for i, block in enumerate(createNotebook(content))
            }
        else: 
            content = splitContent(content)
            blocks = {
                f'block{i}': CodeBlock(text, language).__dict__ 
                for i, text in enumerate(content)
            }    
        page = Page(database_id, name, language, 'Active', *tags[:-1], **blocks)
        res = requests.post(url=url, headers=headers, json=page.__dict__)
        code = res.status_code
        return code

def retrievePage(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    res = requests.get(url, headers=headers)
    print(res.status_code)
    data = res.json()
    writeJson('./notion-app/json/page1.json', data)


