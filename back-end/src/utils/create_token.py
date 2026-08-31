from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

def create_token(data:dict):
    to_encode= data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt



oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
def get_current_user(
    token: str = Depends(oauth_scheme)
):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Not Valid Credential",headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credential_exception

    except JWTError:
        raise credential_exception

    return {"user_id": int(user_id)}