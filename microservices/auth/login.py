from typing import Annotated
from fastapi import APIRouter, Depends, Form, HTTPException, status
import pwd_jwt_operations as operats
from sqlalchemy.ext.asyncio import AsyncSession
from shemas import TokenInfo, UserScheme
from models import AuthModel
from sqlalchemy import select
from database import get_session
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError

router = APIRouter(tags=["JWT"])

oauth2 = OAuth2PasswordBearer(tokenUrl="/login/")

def get_token_payload(
    token: str = Depends(oauth2)
) -> UserScheme:
    try:
        payload = operats.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}"
        )
    return payload

async def validate_jwt(
    payload: dict = Depends(get_token_payload),
    session: AsyncSession = Depends(get_session)
) -> UserScheme:
    
    user_id: str | None = payload.get("sub")
    user_id = int(user_id)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token payload is missing user ID"
        )
    result = await session.execute(
        select(AuthModel).where(AuthModel.id == user_id))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found(jwt token)")
    
    return user

async def validate_auth(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    session: AsyncSession = Depends(get_session)  # Зависимость для получения сессии
):
    result = await session.execute(
        select(AuthModel).where(AuthModel.login == username)
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
        "sub" : str(user.id),
        "username" :user.login,
    }
    token = operats.encode_jwt(payload=jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")

@router.get("/verify_token")
async def verify_token_endpoint(
    user: AuthModel = Depends(validate_jwt)
):
    return {"user_id": user.id} 