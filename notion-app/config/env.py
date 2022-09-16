from pydantic import BaseSettings


class Settings(BaseSettings):
    token: str
    version: str

    class Config:
        env_file = ".env"


settings = Settings()  # type: ignore

headers = {
    "Authorization": f"Bearer {settings.token}",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Notion-Version": settings.version,
}
