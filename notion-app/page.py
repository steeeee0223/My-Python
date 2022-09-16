import requests
from fastapi import UploadFile
from pathlib import PurePath

from .config.env import headers
from .schemas import languages
from .schemas.block import CodeBlock
from .schemas.page import Page
from .utils.util import splitContent, writeJson
from .notebook import createNotebook


# Ignore files and folders
ignore = {
    ".DS_Store",
    "Icon\r",
    ".vscode",
    ".ipynb_checkpoints",
    "__pycache__",
    ".git",
    ".devcontainer",
}


def createPage(database_id: str, file: UploadFile) -> int:
    url = "https://api.notion.com/v1/pages"
    path = file.filename
    obj = PurePath(path)
    tags = obj.parts
    if ignore.intersection(tags):
        return 415  # Unsupported Media Type
    name, ext = obj.stem, obj.suffix

    if ext not in languages:
        return 415  # Unsupported Media Type
    else:
        language = languages[ext]
        content = file.file.read().decode("utf8")
        if ext == ".ipynb":
            block_list = createNotebook(content)
            # pprint(block_list)
            blocks = {f"block{i}": block for i, block in enumerate(block_list)}
        else:
            content = splitContent(content)
            blocks = {
                f"block{i}": CodeBlock(text, language).__dict__
                for i, text in enumerate(content)
            }
        page = Page(database_id, name, language, "Active", *tags[:-1], **blocks)
        res = requests.post(url=url, headers=headers, json=page.__dict__)
        code = res.status_code
        if code != 200:
            print(res.text)
        return code


def retrievePage(page_id: str):
    url = f"https://api.notion.com/v1/pages/{page_id}"
    res = requests.get(url, headers=headers)
    print(res.status_code)
    data = res.json()
    writeJson("./notion-app/json/page1.json", data)
