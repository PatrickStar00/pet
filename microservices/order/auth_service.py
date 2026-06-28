import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
AUTH_ROUTER= os.getenv("AUTH_ROUTER")

async def get_user_id(authorization_header: str) -> int:
    token = (authorization_header or "").strip()
    if token and not token.lower().startswith("bearer "):
        token = f"Bearer {token}"
        
    try:
        async with httpx.AsyncClient() as client:
            auth_response = await client.get(
                AUTH_ROUTER,
                headers={"Authorization": token}
            )
            auth_response.raise_for_status()
            return auth_response.json()["user_id"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail="Ошибка аутентификации"
        )