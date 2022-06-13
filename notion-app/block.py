import requests
import json

# Import from Files
from .schemas.block import CodeBlock

# Fetch token
file = open('notion-app/SECRET.json')
data = json.load(file)
token = data['token']
headers = data['headers']
headers["Authorization"] = f'Bearer {token}'

def writeJson(path: str, data: dict) -> None:
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False)
    
def retrieveBlock(block_id: str) -> None:
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    res = requests.get(url, headers=headers)
    print(res.status_code)
    data = res.json()
    writeJson('./notion-app/json/block.json', data)
    

def createCodeBlock(path: str, language: str) -> CodeBlock:
    content = open(path).read()
    block = CodeBlock(content, language)
    return block
    
