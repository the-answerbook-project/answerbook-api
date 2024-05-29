import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "development")
    testing: bool = bool(os.getenv("TESTING", 0))
