import json
import base64
from bs4 import BeautifulSoup
with open('./notion-app/try/ML.ipynb', 'r') as f:
    file = f.read()


# convert data into dict
file = json.loads(file)


# number of cells
num = len(file['cells']) # 4

def writeImage(img_data, img_name="imageToSave"):
    with open(f"./notion-app/try/{img_name}.png", "wb") as fh:
        fh.write(base64.urlsafe_b64decode(img_data))


for i, cell in enumerate(file['cells']):
    print(f"type = {cell['cell_type']}")
    # list of source code lines
    source: list[str] = cell['source']
    print(len(source))
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

