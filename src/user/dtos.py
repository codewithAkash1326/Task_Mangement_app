
from pydantic import BaseModel

class UserCreate(BaseModel):
    name:str
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username:str
    password:str

class UserCreatedResponse(BaseModel):
    username:str
    name:str
    email:str
    id :int