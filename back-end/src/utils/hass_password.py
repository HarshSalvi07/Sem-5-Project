from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated= 'auto')

def hashpassword(password: str) -> str:
    return pwd_context.hash(password)

def verifyPassword(plain_password: str,password: str) -> bool:
    return pwd_context.verify(plain_password,password)
