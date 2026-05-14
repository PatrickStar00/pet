from pydantic import BaseModel
from datetime import datetime
from typing import List

class OrderItem(BaseModel):
    menu_item_id: int
    quantity: int 

class OrderRequest(BaseModel):
    items: List[OrderItem] 

class AuthResponse(BaseModel):
    user_id: int

class MenuItem(BaseModel):
    id: int
    name: str
    price: int

class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    total_price: int
    status: str
    created_at: datetime
    items: List[OrderItem]