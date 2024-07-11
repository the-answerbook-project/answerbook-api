import httpx
from fastapi import APIRouter, Depends

from api.dependencies import get_settings
from api.settings import Settings

proxy = APIRouter(prefix="/proxy", tags=["proxy"])


@proxy.get("/mathpix-token")
async def get_mathpix_token(
    settings: Settings = Depends(get_settings),
):
    headers = {
        "app_id": settings.mathpix_app_id,
        "app_key": settings.mathpix_app_key,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.mathpix.com/v3/app-tokens",
            headers=headers,
            json={"include_strokes_session_id": True},
        )
        return response.json()
