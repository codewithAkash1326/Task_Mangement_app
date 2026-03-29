
from fastapi import  APIRouter , Depends , status , Request
from src.user import controller
from src.user.dtos import UserCreate , UserCreatedResponse , UserLogin
from src.utils.db import get_db
from sqlalchemy.orm import Session
user_routes = APIRouter(prefix='/users')


@user_routes.post('/register', response_model=UserCreatedResponse, status_code=status.HTTP_201_CREATED)
def register_user(body: UserCreate , db: Session = Depends(get_db)):
    return controller.register_user(body , db)

@user_routes.post('/login' , status_code=status.HTTP_200_OK)
def login(body:UserLogin , db:Session = Depends(get_db)):
    return controller.login(body,db)

@user_routes.get('/is_auth' ,response_model=UserCreatedResponse, status_code=status.HTTP_200_OK)
def is_auth(request:Request , db:Session = Depends(get_db)):
    return controller.is_authenticated(request , db)
