from sqlalchemy import select
from fastapi import FastAPI, Depends, HTTPException

from pwd_operations import check_password, encode_jwt 
from shemas import UserScheme
from models import AuthModel
from database import SessionDep
import register, database, login

app = FastAPI()

app.include_router(register.router)
app.include_router(database.router)
app.include_router(login.router)

# @app.post("/login")
# async def login(data: UserScheme, session: SessionDep):
#     result = await session.execute(
#         select(AuthModel).where(AuthModel.login == data.login)
#     )
#     user = result.scalar_one_or_none()

#     if not user:
#         raise HTTPException(status_code=404, detail="Пользователь не найден")

#     if not check_password(data.password, user.password):
#         raise HTTPException(status_code=401, detail="Неверный пароль")

#     token = encode_jwt({"sub": user.login})
#     return {"access_token": token, "token_type": "bearer"}