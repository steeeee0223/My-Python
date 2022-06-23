from typing import Optional
from .base import CodeText, RichText, Icon     
        
class CodeBlock():
    def __init__(self, content: str, language: str):
        self.object = 'block'
        self.type = 'code'
        self.code = CodeText(content, language).__dict__

class TableOfContent():
    def __init__(self) -> None:
        self.type = 'table_of_contents'
        self.table_of_contents = {"color": "default"}

class Divider():
    def __init__(self) -> None:
        self.type = 'divider'
        self.divider = {}

class Block():
    def __init__(self, block_type: str, content: Optional[str]=None) -> None:
        self.object = 'block'
        self.type = block_type
        self.__setattr__(block_type, RichText(content).__dict__)
        
class Heading(Block):
    def __init__(self, size: int, content: Optional[str] =None) -> None:
        super(Heading, self).__init__(f"heading_{size}", content)

class Paragraph(Block):
    def __init__(self, content: Optional[str] =None) -> None:
        super(Paragraph, self).__init__("paragraph", content)
        
class Quote(Block):
    def __init__(self, content: Optional[str] =None) -> None:
        super(Quote, self).__init__("quote", content)

class Callout(Block):
    def __init__(self, content: Optional[str] =None) -> None:
        super(Callout, self).__init__("callout", content)
        self.__getattribute__('callout')['icon'] = Icon().__dict__

class Todo(Block):
    def __init__(self, content: Optional[str] =None, checked: bool=False) -> None:
        super(Todo, self).__init__("to_do", content)
        self.__getattribute__('to_do')['checked'] = checked

class ListItem(Block):
    def __init__(
            self, list_item: str, content: Optional[str] =None, **items: tuple[str,list]
        ) -> None:
        super(ListItem, self).__init__(list_item, content)
        createChild = lambda item: BLOCK_MAP[item[0]](*item[1]).__dict__
        children = list(map(createChild, items.values()))
        self.__getattribute__(list_item)['children'].extend(children)        

class BulletedList(ListItem):
    def __init__(
        self, content: Optional[str] =None, **items: tuple[str,list]
    ) -> None:
        super(BulletedList, self).__init__("bulleted_list_item", content, **items)
        
class NumberedList(ListItem):
    def __init__(
            self, content: Optional[str] =None, **items: tuple[str,list]
        ) -> None:
        super(NumberedList, self).__init__("numbered_list_item", content, **items)
        
BLOCK_MAP = {
    "table_of_content": TableOfContent,
    "thematic_break": Divider, # divider
    
    "heading": Heading, # f"heading_{level}"
    "paragraph": Paragraph, # "paragraph"
    "block_quote": Quote, # "quote"
    "block_callout": Callout, # "callout"
    "block_code": CodeBlock, # "code"
    "task_list_item": Todo, # "to_do"
    # type: list  
    # ordered: bool =False
    "list_item": ListItem,
    # type: list  
    # ordered: bool

    # "ul": BulletedList, # "bulleted_list_item"
    # "ol": NumberedList # "numbered_list_item"
}


