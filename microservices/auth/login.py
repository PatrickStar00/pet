from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
import pwd_operations as operats
from sqlalchemy.ext.asyncio import AsyncSession
from shemas import TokenInfo, UserScheme
from models import AuthModel
from sqlalchemy import select
from database import get_session

router = APIRouter(prefix="/jwt", tags=["JWT"])


async def validate_auth(
    login: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_session)  # Зависимость для получения сессии
):
    result = await session.execute(
        select(AuthModel).where(AuthModel.login == login)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not user or not operats.check_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )


    return user

@router.post("/login/", response_model=TokenInfo)
async def auth_user(user: UserScheme = Depends(validate_auth)):
    
    
    jwt_payload = {
        "sub" : user.id,
        "username" :user.login,
    }
    token = operats.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")

    
