from .base import Title, Select, MultiSelect


class Parent:
    def __init__(self, database_id: str):
        self.database_id = database_id


class Properties:
    def __init__(self, page_name: str, language: str, status: str, *tags):
        self.Name = Title(page_name).__dict__
        self.Language = Select(language).__dict__
        self.Status = Select(status).__dict__
        self.Tags = MultiSelect(*tags).__dict__


class Page:
    def __init__(
        self,
        database_id: str,
        page_name: str,
        language: str,
        status: str,
        *tags,
        **blocks
    ):
        self.parent = Parent(database_id).__dict__
        self.properties = Properties(page_name, language, status, *tags).__dict__
        self.children = list(blocks.values())
