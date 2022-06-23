import json
import base64
import mistune
from pprint import pprint

from utils.block_callout import plugin_callout
from schemas.block import BLOCK_MAP

with open('./notion-app/try/markdown.ipynb', 'r') as f:
    file = f.read()

# convert data into dict
file = json.loads(file)

# number of cells
num = len(file['cells']) # 4

def writeImage(img_data, img_name="imageToSave"):
    with open(f"./notion-app/try/{img_name}.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(img_data))

for i, cell in enumerate(file['cells']):
    cellType = cell['cell_type']
    if cellType == 'markdown':
        source: str =''.join(cell['source'])
        plugins = ['table', 'task_lists', 'url', 'abbr',
                    'strikethrough', plugin_callout]
        blocks: list[dict] =mistune.markdown(source, renderer='ast', plugins=plugins)
        blockList: list[dict] =[]
        for i, block in enumerate(blocks):
            print(i)
            # pprint(block)
            blockType = block['type']
            if blockType == 'newline': continue

            elif blockType == 'heading':
                level = block['level'] if block['level'] < 4 else 3
                content = ''.join(child['text'] for child in block['children'])

                obj = BLOCK_MAP[blockType](size=level, content=content)
                blockList.append(obj.__dict__)
            elif blockType == 'paragraph':
                pprint(block)
            
            else:
                print(f'{blockType} is in BLOCK_MAP: {blockType in BLOCK_MAP}')
                # pprint(block)
                
            
            print('='*10)


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
