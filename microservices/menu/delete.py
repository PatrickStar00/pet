from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session
from models import MenuModel
from sqlalchemy import select
from shemas import DishFind

router = APIRouter(tags=["DELETE DISH"])

@router.delete("/delete_dish")
async def delete_dish(
    find_dish: DishFind,
    session: AsyncSession = Depends(get_session)):
    
    if not find_dish.id and not find_dish.name:
        raise HTTPException(status_code=400, detail="Укажите id или name для удаления блюда.")

    query = select(MenuModel).where(MenuModel.id == find_dish.id) if id else select(MenuModel).where(MenuModel.name == find_dish.name)
    result = await session.execute(query)
    dish = result.scalar_one_or_none()

    if not dish:
        raise HTTPException(status_code=404, detail="Блюдо не найдено.")

    await session.delete(dish)
    await session.commit()

    return {"status": "success", "message": f"Блюдо '{dish.name}' удалено."}