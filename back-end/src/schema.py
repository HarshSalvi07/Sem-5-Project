from pydantic import BaseModel,EmailStr

class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str
