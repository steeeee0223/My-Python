import re 

def getId(url: str) -> str:
    pattern = r'https://www.notion.so/\w+/([\w-]+-)?(\w+)'   
    result = re.match(pattern, url)
    return result.group(2) if result else 'Invalid Url'
