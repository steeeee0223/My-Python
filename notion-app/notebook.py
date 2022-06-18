import json
import base64
import markdown
from bs4 import BeautifulSoup

with open('./notion-app/try/markdown.ipynb', 'r') as f:
    file = f.read()

# convert data into dict
file = json.loads(file)

# number of cells
num = len(file['cells']) # 4

def writeImage(img_data, img_name="imageToSave"):
    with open(f"./notion-app/try/{img_name}.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(img_data))

def markdownToHtml(source: str) -> str:
    html = markdown.markdown(source)
    return html
    

for i, cell in enumerate(file['cells']):
    cellType = cell['cell_type']
    print(f"type = {cellType}")
    # list of source code lines
    # cell['source']: list[str]
    if cellType == 'markdown':
        source: str =''.join(cell['source'])
        html: str =markdownToHtml(source)
        soup = BeautifulSoup(html, "html.parser") #.contents # list[PageElement]
        print(len(soup))
        
        for count, tag in enumerate(soup.contents):
            if count == 20: break
            if not tag.name: continue
            print(tag.name, tag.get_text(strip=True))
            print('='*10)
            

    print('='*20)


    
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
