from fastapi import FastAPI, Depends, APIRouter, Form, HTTPException, status
from shemas import OrderRequest
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_session
from typing import Annotated
from menu_service import get_menu_item_price
from auth_service import get_user_id
from models import OrderModel, OrderItemModel


router = APIRouter()
app = FastAPI(title="Order Service API")

@router.post("/orders", status_code=201)
async def create_order(
    order_data: OrderRequest,
    session: AsyncSession = Depends(get_session),
    Authorization: str = Annotated[str, Form()]
):
    user_id = await get_user_id(Authorization)

    total_price = 0 
    order_items_list = []

    for item in order_data.items:
        # временно фиксируем цену
        price_at_time_of_order = await get_menu_item_price(item.menu_item_id)
        total_price += price_at_time_of_order * item.quantity

        order_item = OrderItemModel(
            menu_item_id=item.menu_item_id,
            price_at_time_of_order=price_at_time_of_order,
            quantity=item.quantity
        )
        order_items_list.append(order_item)

    new_order = OrderModel(
        user_id=user_id,
        total_price=total_price,
        status="pending",
        items=order_items_list
    )

    session.add(new_order)
    await session.commit()
    await session.refresh(new_order)

    return {"order_id": new_order.id, "total_price": total_price}

@router.get("/my_orders")
async def get_my_orders(
    session: AsyncSession = Depends(get_session),
    Authorization: str = Annotated[str, Form()]
):
    user_id = await get_user_id(Authorization)
    
    result = await session.execute(
        select(OrderModel).where(OrderModel.user_id == user_id)
    )
    orders = result.scalars().all()

    if not orders:
        return {"message": "У пользователя нет заказов"}

    return {"user_id": user_id, "orders": orders}

@router.delete("/delete_order")
async def delete_order(
    order_id: str = Annotated[str, Form()],
    session: AsyncSession = Depends(get_session),
    Authorization: str = Annotated[str, Form()]
):
    user_id = await get_user_id(Authorization)
    
    result = await session.execute(select(OrderModel).where(OrderModel.id == int(order_id)))
    order = result.scalar_one_or_none()
    
    if int(order.id) != int(order_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden access")
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="order not found")
    
    await session.delete(order)
    await session.commit()
    
    return {"message": f"Заказ {order_id} успешно удалён"}