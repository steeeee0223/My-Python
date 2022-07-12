import json
import base64
import mistune
from pprint import pprint

from .utils.block_callout import plugin_callout
from .schemas.block import BLOCK_MAP

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
            try:
                block['info'].index('=')
                language = block['info'].split('=')[0]
            except:
                language = block['info']    
            # language = block['info'].split('=')[0]
            content = block['text']
            obj = BLOCK_MAP[blockType](content, language)
        case 'list_item':
            content = getContent(block['children'][0])
            print(content)
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

def createNotebook(notebook) -> list[dict]:
    
    notebook = json.loads(notebook)

    blockList: list[dict] =[]
    for cell in notebook['cells']:
        match cell:
            case {'cell_type': 'code', 'source': source, **rest}:
                source = ''.join(source)
                block = BLOCK_MAP['block_code'](source, 'python').__dict__
                blockList.append(block)
            case {'cell_type': 'markdown', 'source': source, **rest}:
                source: str =''.join(source)
                plugins = ['table', 'task_lists', 'url', 'abbr',
                            'strikethrough', plugin_callout]
                blocks: list[dict] =mistune.markdown(source, renderer='ast', plugins=plugins)
                for block in blocks:
                    match block['type']:
                        case 'newline': continue
                        case 'thematic_break'|'heading'|'paragraph'|'block_quote' \
                            |'block_callout'|'block_code':
                            blockList.append(createBlock(block))
                        case 'list':
                            items = createList(block)
                            blockList.extend(items)
                        # case _: continue
    return blockList