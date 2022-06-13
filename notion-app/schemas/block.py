from .base import Text

class Code():
    def __init__(self, content: str, language: str):
        self.rich_text = [Text(content).__dict__]
        self.language = language
        
class CodeBlock():
    def __init__(self, content: str, language: str):
        self.object = 'block'
        self.type = 'code'
        self.code = Code(content, language).__dict__
