from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schema
from fastapi import status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

token_secret_key = os.getenv('SECRET_KEY_TOKEN')

#secret_key
#algorithm
#time expiry for token


ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, token_secret_key, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    
    try: 
        payload = jwt.decode(token, token_secret_key, algorithms=[ALGORITHM])
        id : str = payload.get("user_id")
        
        if not id:
            raise credentials_exception
        token_data = schema.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate Credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)