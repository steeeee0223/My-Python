from typing import Optional

color_list = [
    "gray",
    "brown",
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "purple",
    "pink",
]


class Content:
    def __init__(self, content: Optional[str] = None):
        self.content = content


class Text:
    def __init__(self, content: Optional[str] = None):
        self.type = "text"
        self.text = Content(content).__dict__
        # self.annotations = {
        #     "bold": False,
        #     "italic": False,
        #     "strikethrough": False,
        #     "underline": False,
        #     "code": False,
        #     "color": "default"
        # }


class RichText:
    def __init__(self, content: Optional[str] = None) -> None:
        self.rich_text: list[dict] = [Text(content).__dict__]
        self.color = "default"
        self.children = []


class CodeText:
    def __init__(self, content: str, language: str):
        self.rich_text = [Text(content).__dict__]
        self.language = language


class Title:
    def __init__(self, title: Optional[str] = None):
        self.type = "title"
        self.title = [Text(title).__dict__] if title else []


class SelectOptions:
    def __init__(self, name: str, color: Optional[str] = None):
        self.name = name
        if color:
            self.__setattr__("color", color)


class Select:
    def __init__(self, tag: Optional[str] = None):
        self.type = "select"
        self.select = SelectOptions(tag).__dict__ if tag else {}


class MultiSelect:
    def __init__(self, *tags):
        self.type = "multi_select"
        self.multi_select = [SelectOptions(tag).__dict__ for tag in tags]


class CreatedTime:
    def __init__(self) -> None:
        self.type = "created_time"
        self.created_time = {}
        self.name = "Created Time"


class CreatedBy:
    def __init__(self) -> None:
        self.type = "created_by"
        self.created_by = {}
        self.name = "Created By"


class LaseEditedTime:
    def __init__(self) -> None:
        self.type = "last_edited_time"
        self.last_edited_time = {}
        self.name = "Last Edited Time"


class LaseEditedBy:
    def __init__(self) -> None:
        self.type = "last_edited_by"
        self.last_edited_by = {}
        self.name = "Last Edited By"


class Icon:
    def __init__(self, emoji: str = "💡") -> None:
        self.emoji = emoji


property_map = {
    "title": Title().__dict__,
    "multi_select": MultiSelect().__dict__,
    "select": Select().__dict__,
    "created_time": CreatedTime().__dict__,
    "created_by": CreatedBy().__dict__,
    "last_edited_time": LaseEditedTime().__dict__,
    "last_edited_by": LaseEditedBy().__dict__,
}
