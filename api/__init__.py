from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.router import api_router
from api.router.answers import answers_router
from api.router.authentication import authentication_router
from api.router.candidates import candidates_router
from api.router.exam import exam_router
from api.router.marking import marking_router
from api.router.proxy import proxy
from api.router.questions import questions_router
from api.settings import Settings

tags_metadata = [
    {
        "name": "status",
        "description": "API heartbeat",
    },
    {
        "name": "exam",
        "description": "Exam questions and information",
    },
    {
        "name": "marking",
        "description": "Exam marks and answers",
    },
    {
        "name": "proxy",
        "description": "Proxy endpoints to third-party services",
    },
    {
        "name": "authentication",
        "description": "Authentication tokens issuing and revoking",
    },
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

    rest_api.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    rest_api.include_router(api_router)
    rest_api.include_router(candidates_router)
    rest_api.include_router(exam_router)
    rest_api.include_router(questions_router)
    rest_api.include_router(marking_router)
    rest_api.include_router(answers_router)
    rest_api.include_router(authentication_router)
    rest_api.include_router(proxy)

    return rest_api
