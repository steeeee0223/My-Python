data = {
    'level': 4, 
    'children': [{'type': 'block'}]
}

def match(data: dict):
    match data:
        case {'level': 1, **rest}:
            return 'LEVEL 1'
        case {'level': 2, **rest}:
            print(rest)
            return 'LEVEL 2'
        case {'level': _, **rest}:
            return 'OTHER LEVEL'
        case _:
            return 'NO LEVEL'
print(match(data))

lst = ['a','b','c']
print(dict(enumerate(lst)))