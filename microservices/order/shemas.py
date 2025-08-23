from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

# Схема для одного элемента в заказе.
class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int = Field(gt=0)

# Схема для всего тела запроса на создание заказа
class OrderRequest(BaseModel):
    items: List[OrderItem] # список объектов OrderItem

# Схема для данных, которые возвращает Auth Service
class AuthResponse(BaseModel):
    user_id: int
    is_authenticated: bool

# Схема для данных, которые возвращает Menu Service
class MenuItem(BaseModel):
    id: int
    name: str
    price: int

# Схема для ответа, который Order Service вернет клиенту
class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    total_price: int
    status: str
    created_at: datetime
    items: List[OrderItem]