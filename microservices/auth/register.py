from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from main import SessionDep
from pwd_operations import hash_password
from shemas import UserScheme
from models import AuthModel

router = APIRouter(tags=["REGISTRATION"])

@router.post("/register")
async def add_user(data: UserScheme, session: SessionDep):
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