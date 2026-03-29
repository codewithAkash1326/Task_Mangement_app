import jwt
from sqlalchemy.orm import Session
from src.user.dtos import UserCreate , UserCreatedResponse  , UserLogin
from src.user.models import UserModel
from fastapi import HTTPException , Request , status
from pwdlib import PasswordHash
from src.utils.setings import setting
from datetime import datetime , timedelta
from jwt.exceptions import InvalidTokenError
import re

password_hash = PasswordHash.recommended()

def get_hash_password(password):
    return password_hash.hash(password)

def verify_password(plain_password , hashed_password):
    return password_hash.verify(plain_password,hashed_password)

def is_valid_email(email: str):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


def register_user(user_data: UserCreate, db: Session):

    if user_data.username == "":
        raise HTTPException(status_code=400, detail="Username is required")
    elif user_data.email == "":
        raise HTTPException(status_code=400, detail="Email is required")
    elif user_data.password == "":
        raise HTTPException(status_code=400, detail="Password is required")
    elif user_data.name == "":
        raise HTTPException(status_code=400, detail="Name is required")
    elif len(user_data.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long")
    
    is_user_exist = db.query(UserModel).filter((UserModel.username == user_data.username))
    if is_user_exist.first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    is_user_email_exist = db.query(UserModel).filter((UserModel.email == user_data.email))
    if is_user_email_exist.first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if not is_valid_email(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email")

    hashed_password = get_hash_password(user_data.password)

    
    
    new_user = UserModel(
        name=user_data.name,
        username=user_data.username,
        email=user_data.email,
        hash_password=hashed_password
    )
    db.add(new_user)
    db.commit() 
    db.refresh(new_user)

    return UserCreatedResponse( 
        status="Registration Succesfull",
        username=new_user.username,
        name=new_user.name,
        email=new_user.email,
        id=new_user.id
    )



def login(body:UserLogin , db:Session):
    user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if(user is None):
        raise HTTPException(status_code=400 , detail="User name is incorrect")
    
    is_password_matched = verify_password(body.password , user.hash_password)

    if not is_password_matched:
        raise HTTPException(status_code=400 , detail="PASSWORD is incorrect")
    
    exp_time = datetime.now() + timedelta(minutes=setting.EXP_TIME)
    
    token = jwt.encode({"_id":user.id , "exp":exp_time.timestamp() } , setting.SECRET_KEY , setting.ALGORITHM)


    return {
        "message":"Login succesfull" ,
        "token":token
    }
   
    
def is_authenticated(request:Request , db:Session ):
    try:
        headers = request.headers
        token = headers.get("Authorization")

        if not token:
            raise HTTPException(status_code=401 , detail="Token is Empty")
        token = token.split(" ")[-1]

        data = jwt.decode(token , setting.SECRET_KEY , setting.ALGORITHM)

        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id==user_id).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="User not Founf")
        print(data)
        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="you are unauthorized")