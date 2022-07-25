import re 

def getId(url: str) -> str:
    pattern = r'https://www.notion.so/\w+/([\w-]+-)?(\w+)'   
    result = re.match(pattern, url)
    return result.group(2) if result else 'Invalid Url'

def splitContent(s: str, n: int=2000) -> list[str]:
    def _f(s, n):
        while s: yield s[:n]; s = s[n:]
    return list(_f(s, n))