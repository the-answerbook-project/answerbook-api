from pydantic import BaseModel


class Status(BaseModel):
    """The API Status"""

    status: str
    version: str
    environment: str
    testing: bool

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "status": "Answerbook alive",
                    "version": "1.0",
                    "environment": "production",
                    "testing": False,
                }
            ]
        }
    }
