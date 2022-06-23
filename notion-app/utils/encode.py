import json
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, "__dict__"):
            return {key: value for key, value in obj.__dict__.items() if not key.startswith("_")}
        return super().default(obj)

'''
:Example:

obj = SomeClass()
print(json.dumps(obj, cls=ComplexEncoder, indent=4))

'''