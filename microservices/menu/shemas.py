from pydantic import BaseModel
from typing import Optional

class DishCreate(BaseModel):
    name: str
    category: str
    price: int
    description: Optional[str] = None