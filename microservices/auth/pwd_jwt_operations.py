from pydantic import BaseModel
from pathlib import Path
import jwt
import bcrypt
from datetime import datetime, timedelta

class AuthJWT(BaseModel):
    private_key: str = open('certs/jwt-private.pem', 'r').read()
    public_key: str = open("certs/jwt-public.pem", 'r').read()
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    
auth_jwt = AuthJWT()

def encode_jwt(payload: dict, 
               private_key: str = auth_jwt.private_key, 
               algorithm: str = auth_jwt.algorithm,
               expire_minutes: int = auth_jwt.access_token_expire_minutes):
    to_encode = payload.copy()
    now = datetime.utcnow()
    expire = now + timedelta(minutes=expire_minutes)
    
    to_encode.update(exp=expire, iat=now)
    
    encoded = jwt.encode(to_encode, private_key, algorithm = algorithm)
    return encoded

def decode_jwt(token: str, public_key = auth_jwt.public_key, algorithm = auth_jwt.algorithm):
    decoded = jwt.decode(token, public_key, algorithm = algorithm)
    return decoded

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()  # сохраняем str

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())  # type: ignore # снова делаем bytes