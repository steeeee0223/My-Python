from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .dependencies import origins
from .routes import main_router

app = FastAPI()

# Cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static files
app.mount("/static", StaticFiles(directory="notion-app/static"), name="static")

# Routes
app.include_router(main_router)
