from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String
from typing import Optional

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

class MenuModel(Base):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    category: Mapped[str] = mapped_column(String(100))
    price: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)