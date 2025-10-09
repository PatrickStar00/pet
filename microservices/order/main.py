from fastapi import FastAPI, Depends, Header, APIRouter, HTTPException, Form
from sqlalchemy.ext.asyncio import AsyncSession
from shemas import OrderRequest
from database import get_session
from auth_service import get_user_id
from menu_service import get_menu_item_price
from models import OrderItemModel, OrderModel
import database
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated


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

app.include_router(router)
app.include_router(database.router)