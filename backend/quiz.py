from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .main import get_db
from . import models, schemas

router = APIRouter(prefix="/api/quiz", tags=["Quiz API"])

# QUIZ QUESTIONS (STATIC for now)
QUESTIONS = [
    {
        "id": 1,
        "question": "Which country had the highest total travelers?",
        "options": ["USA", "UK", "India", "China"],
        "answer": 0
    },
    {
        "id": 2,
        "question": "What was the global travel spending?",
        "options": ["$399B", "$1.5B", "$9.1T", "$171T"],
        "answer": 3
    },
    {
        "id": 3,
        "question": "Which dashboard shows recovery index?",
        "options": ["Popularity", "Statistics", "Recovery", "Receipts"],
        "answer": 2
    }
]


# ---------------- GET QUIZ QUESTIONS ----------------

@router.get("/questions")
def get_questions():
    # Remove answers before sending to frontend
    safe_questions = [{key: q[key] for key in q if key != "answer"} for q in QUESTIONS]
    return {"questions": safe_questions}


# ---------------- SUBMIT QUIZ ----------------

@router.post("/submit")
def submit_quiz(data: schemas.QuizSubmit, db: Session = Depends(get_db)):
    user_answers = data.answers
    score = 0

    for i, q in enumerate(QUESTIONS):
        if user_answers[i] == q["answer"]:
            score += 1

    result = models.QuizResult(
        user_email=data.user_email,
        score=score,
        total=len(QUESTIONS)
    )
    db.add(result)
    db.commit()

    return {
        "score": score,
        "total": len(QUESTIONS)
    }


# ---------------- SCORE HISTORY ----------------

@router.get("/history/{email}")
def quiz_history(email: str, db: Session = Depends(get_db)):
    history = db.query(models.QuizResult).filter(models.QuizResult.user_email == email).all()
    return history
