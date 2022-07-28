import json
import mistune
from pprint import pprint
import re

from .utils.block_callout import plugin_callout
from .utils.util import splitContent
from .schemas.block import BLOCK_MAP
from .schemas.setting import languages

def getContent(block: dict, content: str='') -> str:
    if not block.get('children'): return ''
    for child in block['children']:
        content += child.get('text', getContent(child))
    return content

def createObjects(block_type: str, content: str, **keys) -> list[dict]:
    contents = splitContent(content)
    return [BLOCK_MAP[block_type](content=x, **keys).__dict__ for x in contents]

def createBlocks(block: dict, list_type: str='') -> list[dict]:
    match (block_type := block['type']):
        case 'thematic_break':
            return [BLOCK_MAP[block_type]().__dict__]
        case 'heading':
            content = getContent(block)
            if block['level'] < 4:
                return createObjects('heading', content=content, level=block['level'])
            else:
                return createObjects('paragraph', content=content)    
        case 'paragraph'|'block_quote':
            content = getContent(block)
            return createObjects(block_type, content=content)
        case 'block_callout':
            header = block['children'][0]['text'] # e.g. info, danger...
            content = getContent(block['children'][1])
            return createObjects(block_type, content=content)
        case 'block_code':
            if block['info']:     
                match = re.match(r'([a-z]*)(=\d*)?', block['info'])            
                language = match.group(1) if match else "plain text"
                if not language in languages.values():
                    language = "plain text"
            else: 
                language = "plain text"
            return createObjects(block_type, content=block['text'], language=language)
        case 'list_item':
            content = getContent(block['children'][0])
            return createObjects(list_type, content=content)
        case 'task_list_item':
            content = getContent(block['children'][0])
            return createObjects('to_do', content=content, checked=block['checked'])
        case _:
            pprint(block)
            print('WILDCARD CASE')
            return []

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
            children.extend(createBlocks(item, list_type))
        items = [BLOCK_MAP[list_type](content, *children).__dict__]
    else:
        items = createBlocks(data, list_type)
    return items

def createList(data: dict) -> list[dict]:
    '''
    data = {'type': 'list', 'ordered': bool, 'children': [...]}
    '''
    list_type = 'numbered' if data['ordered'] else 'bulleted'
    items = []
    for item in data['children']:
        items.extend(createListItem(item, list_type))
    return items

def getOutputContent(data: dict) -> str:
    '''
    data = {'text/plain': list[str]}
    data = {'text/html': list[str]}
    data = {'image/png': str}
    '''
    res = ''
    if data.get('text/plain'):
        res += ''.join(data['text/plain']) + '\n'
    if data.get('image/png'):
        content = data['image/png']
        res += '*** IMAGE OUTPUT ***\n'
    return res

def getOutput(output: dict) -> str:
    match output:
        case {'output_type': 'stream', 'text': text, **rest}:
            return ''.join(text)
        case {'output_type': 'error', 'ename': ename, 'evalue': evalue, **rest}:
            return f"{ename}: {evalue}"
        case {'output_type': 'execute_result', 'data': data, **rest}:
            return getOutputContent(data)
        case {'output_type': 'display_data', 'data': data, **rest}:
            return getOutputContent(data)
        case _:
            return ''

def createNotebook(notebook) -> list[dict]:
    notebook = json.loads(notebook)
    blockList: list[dict] =[]

    for cell in notebook['cells']:
        match cell:
            case {'cell_type': 'code', 'source': source, 'outputs': outputs, **rest}:
                content = ''.join(source)
                if outputs:
                    content += '\n>>>\n' + ''.join(map(getOutput, outputs))
                blocks = createObjects('block_code', content=content, language="python")
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
                            blockList.extend(createBlocks(block))
                        case 'list':
                            blockList.extend(createList(block))
                        # case _: continue
    return blockList