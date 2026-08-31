from utils import create_token, hass_password
from database import get_db
from models import User
from fastapi import FastAPI, Depends, HTTPException, status
from schema import RegisterSchema
from sqlalchemy.orm import Session

app = FastAPI()

@app.post('/register')
def register(user: RegisterSchema,db: Session = Depends(get_db) ):
    userExist = db.query(User).filter(User.email == user.email).first()
    if userExist :
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="User Already Exist")

    hass_Pass = hass_password.hashpassword(user.password)

    new_user = User(
        username = user.username,
        email = user.email,
        password = hass_Pass
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"Message": "Signup Successfull"}