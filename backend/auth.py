from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY", "")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")
ALGORITHM: str = os.getenv("ALGORITHM", "")
if not ALGORITHM:
    raise ValueError("ALGORITHM environment variable is not set")

pwd_context = CryptContext(schemes=["argon2"])

def hash_password(password):
    return pwd_context.hash(password)

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)


def create_token(user_id):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(hours=4),
    }
    print("Creating token with :", payload)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    


def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
