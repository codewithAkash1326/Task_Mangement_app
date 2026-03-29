from fastapi import Request , status , HTTPException ,Depends
from src.user.models import UserModel
from sqlalchemy.orm import Session
from src.user.dtos import UserCreatedResponse
from jwt import InvalidTokenError
from src.utils.setings import setting
from src.utils.db import get_db
import jwt 

def is_authenticated(request:Request , db:Session = Depends(get_db) ):
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
        return UserCreatedResponse( 
            status="Authenticated user",
            username=user.username,
            name=user.name,
            email=user.email,
            id=user.id
        )
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="you are unauthorized")