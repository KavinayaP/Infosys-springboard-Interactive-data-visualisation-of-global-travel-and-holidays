from fastapi import Depends, HTTPException
from datetime import datetime, timedelta
from jose import jwt
import bcrypt

SECRET_KEY = "SUPERSECRET"
ALGORITHM = "HS256"

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode())

def create_token(data: dict):
    expires = datetime.utcnow() + timedelta(hours=5)
    data.update({"exp": expires})
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
