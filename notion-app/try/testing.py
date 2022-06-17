from pathlib import PurePath
import os

dic = {'object': list(), 'name': 'List', 'tags': '2'}
name = dic['name']
print(name)
# print(globals())

print(dic.get('n', 'default'))


path = PurePath('./notion-app/json/block.json')

# print(path.parts)   # >>> ('notion-app', 'json', 'block.json')
# print(path.stem)    # >>> block
# print(path.suffix)  # >>> .json

ignore = {'.DS_Store', 'Icon\r', 
          '.vscode', '.ipynb_checkpoints', '__pycache__', '.get', 
          '.devcontainer'}


def list_files(directory: str) -> list:
    res = []
    for (dir_path, dir_names, file_names) in os.walk(directory):
        path = PurePath(dir_path).stem
        if path in ignore: continue
        print(f'Scanning through directory: {dir_path} ...')
        res.extend(_ for _ in file_names if _ not in ignore)
        
    return res

print(list_files('../Test'))

file_list = list_files('../Test')
getType = lambda x: PurePath(x).suffix
file_type = list(map(getType, file_list))
print(file_list)
print(file_type)

tup = 1,2,3
print(tup[:-1])