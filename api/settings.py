import os
from pathlib import Path

DEV_ASSESSMENTS_DIR = Path(__file__).parent.parent / "dev_data"

from pydantic_settings import BaseSettings


def _get_assessment_dir() -> Path:
    if str_path := os.environ.get("ASSESSMENTS_DIR"):
        return Path(str_path)
    return DEV_ASSESSMENTS_DIR


class Settings(BaseSettings):
    environment: str = os.getenv("ENVIRONMENT", "development")
    assessments_dir: Path = _get_assessment_dir()
    testing: bool = bool(os.getenv("TESTING", 0))
