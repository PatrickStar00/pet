from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import MenuModel
from sqlalchemy import select

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
    
@router.get("/price")
async def get_price_by_id(
    id: int | None = None,
    name: str | None = None,
    session: AsyncSession = Depends(get_session)
):
    query = None

    if id is not None:
        query = select(MenuModel.price).where(MenuModel.id == id)
    elif name is not None:
        query = select(MenuModel.price).where(MenuModel.name == name)
    else:
        raise HTTPException(status_code=400, detail="Укажите id или name блюда")

    result = await session.execute(query)
    price = result.scalar_one_or_none()

    if price is None:
        raise HTTPException(status_code=404, detail="Блюдо не найдено")

    return {"price": price}