from fastapi import APIRouter, HTTPException, Form, Depends
from sqlalchemy import select
from pwd_jwt_operations import hash_password
from shemas import UserScheme
from models import AuthModel
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_session

router = APIRouter(tags=["REGISTRATION"])

@router.post("/register")
async def add_user(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_session)):
    
    
    data = UserScheme(login=login, password=password)
    result = await session.execute(select(AuthModel).where(AuthModel.login == data.login))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=409,  
            detail=f"Логин '{data.login}' уже занят"
        )
        
    hashed = hash_password(data.password)
    new_user = AuthModel(
        login=data.login,
        password=hashed
    )
    
    session.add(new_user)
    await session.commit()
    return f"Пользователь {new_user.login} зарегистрирован"