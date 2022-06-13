from .base import property_map, Text, SelectOptions, Select

class Parent:
    def __init__(self, page_id: str) -> None:
        self.type = "page_id"
        self.page_id = page_id

class Properties:
    def __init__(self, **properties) -> None:
        for key, val in properties.items():
            self.__setattr__(key, property_map[val])
        self.Status = Select().__dict__
        self.Status["select"]["options"] = [
            SelectOptions("Active", "green").__dict__,
            SelectOptions("Inactive", "red").__dict__
        ]

class Database:
    def __init__(self, page_id: str, db_name: str, **properties) -> None:
        self.parent = Parent(page_id).__dict__
        self.title = [Text(db_name).__dict__]
        self.properties = Properties(**properties).__dict__
