from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import MenuModel
from sqlalchemy import select


router = APIRouter(tags=["MENU"])
@router.post("/menu")
async def check_menu(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(MenuModel))
    menu_items = result.scalars().all()  # список объектов MenuModel
    
    return [
        {
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "description": item.description
        }
        for item in menu_items
    ]