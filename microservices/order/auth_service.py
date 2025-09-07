import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_SERVICE_URL = os.getenv("AUTH_URL")

async def get_user_id(authorization_header: str) -> int:
    try:
        async with httpx.AsyncClient() as client:
            auth_response = await client.get(
                AUTH_SERVICE_URL,
                headers={"Authorization": authorization_header}
            )
            auth_response.raise_for_status()
            return auth_response.json()["user_id"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Ошибка аутентификации"
        )