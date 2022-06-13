from typing import Optional

color_list = ["gray", "brown", "red", "orange", "yellow", "green", "blue", "purple", "pink"]

class Content:
    def __init__(self, content: Optional[str] =None):
        self.content = content

class Text:
    def __init__(self, content: Optional[str] =None):
        self.type = 'text'
        self.text = Content(content).__dict__ 

class Title:
    def __init__(self, title: Optional[str] =None):
        self.type = 'title'
        self.title = [Text(title).__dict__] if title else []

class SelectOptions:
    def __init__(self, name: str, color: Optional[str] =None):
        self.name = name
        if color: self.__setattr__("color", color)

class Select:
    def __init__(self, tag: Optional[str] =None):
        self.type = 'select'
        self.select = SelectOptions(tag).__dict__ if tag else {}

class MultiSelect:
    def __init__(self, *tags):
        self.type = 'multi_select'
        self.multi_select = [SelectOptions(tag).__dict__ for tag in tags]

property_map = {
    "title": Title().__dict__,
    "multi_select": MultiSelect().__dict__,
    "select": Select().__dict__
}
