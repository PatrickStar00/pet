from fastapi import APIRouter, Depends
import pwd_operations as operats
from main import UserScheme
from shemas import TokenInfo

router = APIRouter(prefix="/jwt", tags=["JWT"])

def validate_auth():
    pass

@router.post("/login/", response_model=TokenInfo)
def auth_user(user: UserScheme = Depends(validate_auth)):
    
    jwt_payload = {
        "sub" : user.id,
        "username" :user.username,
    }
    token = operats.encode_jwt({"sub": user.login})
    return TokenInfo(access_token=token, token_type="Bearer")

    
