from fastapi import FastAPI

from api.router import api_router
from api.settings import Settings

tags_metadata = [
    {
        "name": "status",
        "description": "API heartbeat",
    }
]


def create_application() -> FastAPI:
    rest_api: FastAPI = FastAPI(
        title="Answerbook API",
        description=("API for Answerbook, the digital exam system"),
        version="1.0",
        contact={
            "name": "Ivan Procaccini",
            "url": "https://linktr.ee/ivanproca",
            "email": "ivanprocaccini905@gmail.com",
        },
        openapi_tags=tags_metadata,
        docs_url="/",
    )
    rest_api.include_router(api_router)

    return rest_api
