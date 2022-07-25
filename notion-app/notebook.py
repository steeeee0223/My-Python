import json
import mistune
from pprint import pprint
import re

from .utils.block_callout import plugin_callout
from .utils.util import splitContent
from .schemas.block import BLOCK_MAP

def getContent(block: dict, content: str='') -> str:
    if not block.get('children'): return ''
    for child in block['children']:
        content += child.get('text', getContent(child))
    return content

def parseBlock(block: dict, list_type: str='') -> list[dict]:
    match (blockType := block['type']):
        case 'thematic_break':
            objects = [BLOCK_MAP[blockType]().__dict__]
        case 'heading':
            content = getContent(block)
            if block['level'] < 4:
                objects = createBlocks('heading', content=content, level=block['level'])
            else:
                objects = createBlocks('paragraph', content=content)    
        case 'paragraph'|'block_quote':
            content = getContent(block)
            objects = createBlocks(blockType, content=content)
        case 'block_callout':
            header = block['children'][0]['text'] # e.g. info, danger...
            content = getContent(block['children'][1])
            objects = createBlocks(blockType, content=content)
        case 'block_code':
            match = re.match(r'([a-z]+)(=\d*)?', block['info'])
            language = match.group(1) if match else "plain text"
            objects = createBlocks(blockType, content=block['text'], language=language)
        case 'list_item':
            content = getContent(block['children'][0])
            objects = createBlocks(list_type, content=content)
        case 'task_list_item':
            content = getContent(block['children'][0])
            objects = createBlocks('to_do', content=content, checked=block['checked'])
        case _:
            pprint(block)
            print('WILDCARD CASE')
            objects = []
    return objects

def createBlocks(block_type: str, content: str, **keys) -> list[dict]:
    contents = splitContent(content)
    objects = [BLOCK_MAP[block_type](content=x, **keys).__dict__ for x in contents]
    return objects

def createListItem(data: dict, list_type: str) -> list[dict]:
    '''
    FOR AT MOST LEVEL 2
    data = {'type': 'list_item', 'children': [...]}
    data = {'type': 'task_list_item', 'children': [...]}
    '''
    if len(data['children']) > 1:
        content, rest = data['children']
        content = getContent(content)        
        children = []
        for item in rest['children']:
            children.extend(parseBlock(item, list_type))
        obj = [BLOCK_MAP[list_type](content, *children).__dict__]
    else:
        obj = parseBlock(data, list_type)
    return obj

def createList(data: dict) -> list[dict]:
    '''
    data = {'type': 'list', 'ordered': bool, 'children': [...]}
    '''
    list_type = 'numbered' if data['ordered'] else 'bulleted'
    items = []
    for item in data['children']:
        items.extend(createListItem(item, list_type))
    return items

def createNotebook(notebook) -> list[dict]:
    
    notebook = json.loads(notebook)

    blockList: list[dict] =[]
    for cell in notebook['cells']:
        match cell:
            case {'cell_type': 'code', 'source': source, **rest}:
                blocks = createBlocks('block_code', content=''.join(source), language="python")
                blockList.extend(blocks)
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
                            blockList.extend(parseBlock(block))
                        case 'list':
                            blockList.extend(createList(block))
                        # case _: continue
    return blockList