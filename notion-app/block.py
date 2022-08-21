import requests

from .config.env import headers
from .utils.util import writeJson
from .schemas.block import CodeBlock


def retrieveBlock(block_id: str) -> None:
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    res = requests.get(url, headers=headers)
    print(res.status_code)
    data = res.json()
    writeJson("./notion-app/json/block.json", data)


def createCodeBlock(path: str, language: str) -> CodeBlock:
    content = open(path).read()
    block = CodeBlock(content, language)
    return block
