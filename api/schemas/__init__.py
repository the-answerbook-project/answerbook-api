from datetime import datetime, timezone

from sqlmodel import SQLModel


class BaseSchema(SQLModel):
    class Config:
        json_encoders = {
            datetime: lambda dt: (
                dt.replace(tzinfo=timezone.utc).isoformat() if dt else None
            ),
        }
