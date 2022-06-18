from .base import Text

class Icon():
    def __init__(self, emoji: str="💡") -> None:
        self.emoji = emoji       

class Code():
    def __init__(self, content: str, language: str):
        self.rich_text = [Text(content).__dict__]
        self.language = language
        
class CodeBlock():
    def __init__(self, content: str, language: str):
        self.object = 'block'
        self.type = 'code'
        self.code = Code(content, language).__dict__

class TextBlock():
    def __init__(self, content: str="") -> None:
        self.rich_text: list[dict] = [Text(content).__dict__]
        self.color = "default"
        self.children = []

class Block():
    def __init__(self, block_type: str, content: str="") -> None:
        self.object = 'block'
        self.type = block_type
        self.__setattr__(block_type, TextBlock(content).__dict__)
        
class HeadingBlock(Block):
    def __init__(self, size: int, content: str="") -> None:
        super(HeadingBlock, self).__init__(f"heading_{size}", content)

class ParagraphBlock(Block):
    def __init__(self, content: str="") -> None:
        super(ParagraphBlock, self).__init__("paragraph", content)
        
class QuoteBlock(Block):
    def __init__(self, content: str="") -> None:
        super(QuoteBlock, self).__init__("quote", content)

class CalloutBlock(Block):
    def __init__(self, content: str="") -> None:
        super(CalloutBlock, self).__init__("callout", content)
        self.__getattribute__('callout')['icon'] = Icon().__dict__

class TodoBlock(Block):
    def __init__(self, content: str="", checked: bool=False) -> None:
        super(TodoBlock, self).__init__("to_do", content)
        self.__getattribute__('to_do')['checked'] = checked

class ListItemBlock(Block):
    def __init__(self, list_item: str, content: str="", **items: tuple[str,list]) -> None:
        super(ListItemBlock, self).__init__(list_item, content)
        createChild = lambda item: BLOCK_MAP[item[0]](*item[1]).__dict__
        children = list(map(createChild, items.values()))
        self.__getattribute__("bulleted_list_item")['children'].extend(children)        

class BulletedList(ListItemBlock):
    def __init__(self, content: str="", **items: tuple[str,list]) -> None:
        super(BulletedList, self).__init__("bulleted_list_item", content, **items)
        
class NumberedList(ListItemBlock):
    def __init__(self, content: str="", **items: tuple[str,list]) -> None:
        super(NumberedList, self).__init__("numbered_list_item", content, **items)
        
BLOCK_MAP = {
    "heading_1": HeadingBlock,
    "heading_2": HeadingBlock,
    "heading_3": HeadingBlock,
    "paragraph": ParagraphBlock,
    "quote": QuoteBlock,
    "callout": CalloutBlock,
    "to_do": TodoBlock,
    "bulleted_list_item": BulletedList,
    "numbered_list_item": NumberedList
}


