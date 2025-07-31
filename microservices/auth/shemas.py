from pydantic import BaseModel

class UserScheme(BaseModel):  # модель для добавления в бд
    login: str
    password: str

class UserShema(UserScheme):  # для ответа (с id)
    id: int
    
class TokenInfo(BaseModel):
    access_token: str
    token_type: str