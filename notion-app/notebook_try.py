import json
import base64
from typing import Optional
import mistune
from pprint import pprint

from utils.block_callout import plugin_callout
from schemas.block import BLOCK_MAP

with open('./notion-app/sample/ML.ipynb', 'r') as f:
    file = f.read()

# convert data into dict
file = json.loads(file)
# pprint(file)

# number of cells
num = len(file['cells']) # 4

def writeImage(img_data, img_name="imageToSave"):
    with open(f"./notion-app/try/{img_name}.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(img_data))

def getContent(block: dict, content: str='') -> str:
    if not block.get('children'): return ''
    for child in block['children']:
        content += child.get('text', getContent(child))
    return content

def createBlock(block: dict, list_type: str='') -> dict:
    match (blockType := block['type']):
        case 'thematic_break':
            obj = BLOCK_MAP[blockType]()
        case 'heading':
            level = block['level'] if block['level'] < 4 else 3
            content = getContent(block)
            obj = BLOCK_MAP[blockType](level, content)
        case 'paragraph'|'block_quote':
            content = getContent(block)
            obj = BLOCK_MAP[blockType](content)
        case 'block_callout':
            header = block['children'][0]['text'] # e.g. info, danger...
            content = getContent(block['children'][1])
            obj = BLOCK_MAP[blockType](content)
        case 'block_code':
            language = block['info'].split('=')[0]
            content = block['text']
            obj = BLOCK_MAP[blockType](content, language)
        case 'list_item':
            content = getContent(block['children'][0])
            obj = BLOCK_MAP[list_type](content)
        case 'task_list_item':
            content = getContent(block['children'][0])
            checked = block['checked']
            obj = BLOCK_MAP['to_do'](content, checked)
        case _:
            pprint(block)
            print('WILDCARD CASE')
            obj = []
    return obj.__dict__

def createListItem(data: dict, list_type: str) -> dict:
    '''
    FOR AT MOST LEVEL 2
    data = {'type': 'list_item', 'children': [...]}
    data = {'type': 'task_list_item', 'children': [...]}
    '''
    if len(data['children']) > 1:
        content, rest = data['children']
        content = getContent(content)        
        children = [createBlock(item, list_type) for item in rest['children']]
        obj = BLOCK_MAP[list_type](content, *children).__dict__
    else:
        obj = createBlock(data, list_type)
    return obj

def createList(data: dict) -> list:
    '''
    data = {'type': 'list', 'ordered': bool, 'children': [...]}
    '''
    list_type = 'numbered' if data['ordered'] else 'bulleted'
    items = [createListItem(item, list_type) for item in data['children']]
    return items

def getOutputContent(data: dict):
    '''
    data = {'text/plain': list[str]}
    data = {'text/html': list[str]}
    data = {'image/png': str}
    '''
    if data.get('text/plain'):
        content = ''.join(data['text/plain'])
        print(content)
    if data.get('image/png'):
        content = data['image/png']
        print('IMAGE OUTPUT')

def createOutput(output: dict):
    match output:
        case {'output_type': 'stream', 'text': text, **rest}:
            print('STANDARD OUTPUT')
            content = ''.join(text)
            print(content)
        case {'output_type': 'error', 'ename': ename, 'evalue': evalue, **rest}:
            print('ERROR OUTPUT')
            content = f"{ename}: {evalue}"
            print(content)
        case {'output_type': 'execute_result', 'data': data, **rest}:
            print('EXECUTE OUTPUT')
            getOutputContent(data)

        case {'output_type': 'display_data', 'data': data, **rest}:
            print('DISPLAY OUTPUT')
            getOutputContent(data)
        
        case _:
            print("OTHER")
            pprint(output)


blockList: list[dict] =[]
for i, cell in enumerate(file['cells']):
    match cell:
        case {'cell_type': 'code', 'source': source, 'outputs': outputs, **rest}:
            for output in outputs:
                createOutput(output)


            source = ''.join(source)
            block = BLOCK_MAP['block_code'](source, 'python')
            blockList.append(block)
        case {'cell_type': 'markdown', 'source': source, **rest}:
            source: str =''.join(source)
            plugins = ['table', 'task_lists', 'url', 'abbr',
                        'strikethrough', plugin_callout]
            blocks: list[dict] =mistune.markdown(source, renderer='ast', plugins=plugins)
            for i, block in enumerate(blocks):
                print(i)
                blockType = block['type']
                match blockType:
                    case 'newline': continue
                    case 'thematic_break'|'heading'|'paragraph'|'block_quote' \
                        |'block_callout'|'block_code':
                        blockList.append(createBlock(block))
                    case 'list':
                        items = createList(block)
                        blockList.extend(items)
                    case _:
                        print(f'{blockType} is in BLOCK_MAP: {blockType in BLOCK_MAP}')
                        # pprint(block)          
                print('='*10)
        # case {'outputs': outputs, **rest}:
        #     print('='*10)
        #     print('outputs')
        #     pprint(outputs)
        #     print('='*10)
        case _:
            pprint(cell)


'''
    if (outputs := cell.get('outputs')):
        for output in outputs:
            if output.get('name') == 'stdout': 
                # the real output result
                # list of output text lines
                res: list[str] = output['text']  
            if output.get('output_type') == 'error':
                # the error message
                err = f"{output['ename']}: {output['evalue']}"
            if (data := output.get('data')):
                if data.get('text/plain'):
                    # list of plain text lines
                    res: list[str] = data['text/plain']
                if data.get('text/html'):
                    # list of html text lines
                    html: list[str] = data['text/html']
                if data.get('image/png'):
                    # string of encoded image
                    img: str = data['image/png']
                    writeImage(img)

    print('='*20)
'''    
