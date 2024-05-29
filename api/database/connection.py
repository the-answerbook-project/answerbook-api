import os

from sqlmodel import create_engine

DEV_URL = "postgresql://user:pass@localhost"
FULL_DB_URL: str = os.environ.get("DB_URL", f"{DEV_URL}/answerbook")

engine = create_engine(FULL_DB_URL)
