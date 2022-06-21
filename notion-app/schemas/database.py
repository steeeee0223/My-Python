from .base import property_map, Text, SelectOptions

class Parent:
    def __init__(self, page_id: str) -> None:
        self.type = "page_id"
        self.page_id = page_id

class Properties:
    def __init__(self, **properties) -> None:
        for key, val in properties.items():
            self.__setattr__(key, property_map[val])
        self.Status = property_map["select"]
        self.Status["select"]["options"] = [
            SelectOptions("Active", "green").__dict__,
            SelectOptions("Inactive", "red").__dict__
        ]

class Database:
    def __init__(self, page_id: str, db_name: str, **properties) -> None:
        self.parent = Parent(page_id).__dict__
        self.title = [Text(db_name).__dict__]
        self.properties = Properties(**properties).__dict__
        self.properties['Created Time'] = property_map["created_time"]
        self.properties['Created By'] = property_map["created_by"]
        self.properties['Last Edited Time'] = property_map["last_edited_time"]
        self.properties['Last Edited By'] = property_map["last_edited_by"]