from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class QuizSubmit(BaseModel):
    user_email: str
    answers: list[int]

class QuizResponse(BaseModel):
    score: int
    total: int

