from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import MenuModel
from shemas import DishCreate


router = APIRouter(tags=["ADD DISH"])

@router.post("/add_dish")
async def add_dish(
    dish: DishCreate,
    session: AsyncSession = Depends(get_session)):
    
    new_dish = MenuModel(
        name=dish.name,
        category=dish.category,
        price=dish.price,
        description=dish.description,
    )

    session.add(new_dish)
    await session.commit()
    return f"Блюдо {new_dish.name} добавлено в меню"