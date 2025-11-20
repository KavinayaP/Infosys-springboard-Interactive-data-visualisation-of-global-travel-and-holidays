from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

# FORCE load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env"))


from .database import Base, engine, SessionLocal
from . import models, schemas, auth



Base.metadata.create_all(bind=engine)

app = FastAPI()


from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "Backend running successfully"}



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#chatbot routes
from .chat import router as chat_router
app.include_router(chat_router)

from .voice import router as voice_router
app.include_router(voice_router)

from .quiz import router as quiz_router
app.include_router(quiz_router)




@app.post("/register")
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    check = db.query(models.User).filter(models.User.email == user.email).first()
    if check:
        raise HTTPException(400, "Email already registered")

    new_user = models.User(
        username=user.username,
        email=user.email,
        password=auth.hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}


@app.post("/login")
def login(data: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    if not auth.verify_password(data.password, user.password):
        raise HTTPException(401, "Wrong password")

    token = auth.create_token({"id": user.id, "email": user.email})

    return {"token": token, "username": user.username}
