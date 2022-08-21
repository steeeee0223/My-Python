from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="notion-app/templates")

# cors
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]
