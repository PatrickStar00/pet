import httpx
from fastapi import HTTPException
from dotenv import load_dotenv
import os

load_dotenv()
MENU_SERVICE_BASE_URL = os.getenv("MENU_URL")

async def get_menu_item_price(item_id: int) -> int:
    try:
        async with httpx.AsyncClient() as client:
            menu_response = await client.get(f"{MENU_SERVICE_BASE_URL}/{item_id}")
            menu_response.raise_for_status()
            menu_item_data = menu_response.json()
            return menu_item_data["price"]
    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=404,
            detail=f"Блюдо с ID {item_id} не найдено в меню"
        )