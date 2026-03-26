from sqlalchemy.orm import Session
from src.user.dtos import UserCreate , UserCreatedResponse  , UserLogin
from src.user.models import RegisterUser
from fastapi import HTTPException
from pwdlib import PasswordHash
from email_validator import validate_email, EmailNotValidError

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
    
    is_user_exist = db.query(RegisterUser).filter((RegisterUser.username == user_data.username))
    if is_user_exist.first():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    is_user_email_exist = db.query(RegisterUser).filter((RegisterUser.email == user_data.email))
    if is_user_email_exist.first():
        raise HTTPException(status_code=400, detail="Email already exists")

    if not is_valid_email(user_data.email):
        raise HTTPException(status_code=400, detail="Invalid email")

    hashed_password = get_hash_password(user_data.password)

    
    
    new_user = RegisterUser(
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
    user = db.query(RegisterUser).filter(RegisterUser.username == body.username).first()

    if(user is None):
        raise HTTPException(status_code=400 , detail="User name is incorrect")
    
    is_password_matched = verify_password(body.password , user.hash_password)

    if is_password_matched :
        return {
            "status":"Login done",
        }
    else :
        raise HTTPException(status_code=400 , detail="PASSWORD is incorrect")
    
    