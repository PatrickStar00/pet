from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

# Базовый класс для всех моделей
class Base(DeclarativeBase):
    pass

# Модель таблицы users
class AuthModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))