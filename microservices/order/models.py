from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, ForeignKey
from datetime import datetime

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

class OrderModel(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)  # кто заказал
    items: Mapped[str] = mapped_column(String, nullable=False)  # JSON-строка со списком блюд
    total_price: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(String, default="pending")  # pending / cooking / delivering / completed
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)