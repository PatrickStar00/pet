from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, ForeignKey, DateTime
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    pass

class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Отношение: один заказ имеет много позиций
    items: Mapped[List["OrderItemModel"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )

class OrderItemModel(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True) # Связь с таблицей "orders"
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id")) # ID блюда из menu service
    menu_item_id: Mapped[int] = mapped_column(Integer, nullable=False)
    price_at_time_of_order: Mapped[int] = mapped_column(Integer, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    # Отношение: позиция принадлежит одному заказу
    order: Mapped["OrderModel"] = relationship(back_populates="items")