from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import MenuModel
from sqlalchemy import select
from typing import Annotated


router = APIRouter(tags=["MENU"])
@router.get("/menu")
async def check_menu(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(MenuModel))
    menu_items = result.scalars().all()  # список объектов MenuModel
    
    return [
        {
            "id": item.id,
            "name": item.name,
            "category": item.category,
            "price": item.price,
            "description": item.description
        }
        for item in menu_items
    ]
    
@router.get("/menu/{id}/price")
async def get_price_by_id(
    id: int,
    session: AsyncSession = Depends(get_session)
):
    query = select(MenuModel.price).where(MenuModel.id == id)
    result = await session.execute(query)
    price = result.scalar_one_or_none()
    
    if price is None:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")
    
    return {"price": price}