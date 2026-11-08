from app.models import InterviewAnswer
from app.evaluator import evaluate_answer
from app.models import InterviewAnswer
from app.schemas import InterviewAnswerCreate, InterviewAnswerResponse

from app.question_bank import get_questions

from app.schemas import InterviewSessionCreate, InterviewSessionResponse
from app.models import InterviewSession

from fastapi.security import OAuth2PasswordBearer
from app.security import get_user_id_from_token

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import verify_password, create_access_token 

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse
from app.security import hash_password

from sqlalchemy import text
from app.database import engine

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.database import Base, engine
from app import models

app = FastAPI(title="AI Mock Interview Platform")
Base.metadata.create_all(bind=engine)

# Locate the frontend folder in the project
FRONTEND_DIR = Path(__file__).resolve().parents[2] / "frontend"

# Serve CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static"
)


@app.get("/")
def home():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/db-health")
def database_health():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {"database": "connected"}


@app.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == user_data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is already registered",
        )

    new_user = User(
        email=user_data.email,
        hashed_password=hash_password(user_data.password),
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not user or not verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@app.get("/me")
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at,
    }

@app.post(
    "/interviews",
    response_model=InterviewSessionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_interview(
    interview_data: InterviewSessionCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    session = InterviewSession(
        user_id=user_id,
        role=interview_data.role,
        experience_level=interview_data.experience_level,
        topic=interview_data.topic,
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    return session

@app.get("/interviews/{session_id}/questions")
def get_interview_questions(
    session_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    session = db.query(InterviewSession).filter(
        InterviewSession.id == session_id,
        InterviewSession.user_id == user_id,
    ).first()

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found",
        )
    questions = get_questions(
    topic=session.topic,
    role=session.role,
    experience_level=session.experience_level,
    count=5
)

    return {
        "session_id": session.id,
        "role": session.role,
        "experience_level": session.experience_level,
        "topic": session.topic,
        "questions": questions,
    }

@app.post(
    "/answers",
    response_model=InterviewAnswerResponse,
    status_code=status.HTTP_201_CREATED,
)
def submit_answer(
    answer_data: InterviewAnswerCreate,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    session = db.query(InterviewSession).filter(
        InterviewSession.id == answer_data.session_id,
        InterviewSession.user_id == user_id,
    ).first()

    if session is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview session not found",
        )

    saved_answer = InterviewAnswer(
        session_id=answer_data.session_id,
        question=answer_data.question,
        answer=answer_data.answer,
    )

    db.add(saved_answer)
    db.commit()
    db.refresh(saved_answer)

    return saved_answer

@app.post("/answers/{answer_id}/evaluate")
def evaluate_saved_answer(
    answer_id: int,
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    saved_answer = (
        db.query(InterviewAnswer)
        .join(InterviewSession)
        .filter(
            InterviewAnswer.id == answer_id,
            InterviewSession.user_id == user_id,
        )
        .first()
    )

    if saved_answer is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Answer not found",
        )

    result = evaluate_answer(
    saved_answer.answer,
    saved_answer.question
)

    saved_answer.score = result["score"]
    saved_answer.feedback = result["feedback"]

    db.commit()
    db.refresh(saved_answer)

    return {
        "answer_id": saved_answer.id,
        "score": saved_answer.score,
        "feedback": saved_answer.feedback,
    }

@app.get("/interviews")
def get_interview_history(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user_id = get_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    sessions = (
        db.query(InterviewSession)
        .filter(InterviewSession.user_id == user_id)
        .order_by(InterviewSession.created_at.desc())
        .all()
    )

    history = []

    for session in sessions:
        answers = (
            db.query(InterviewAnswer)
            .filter(InterviewAnswer.session_id == session.id)
            .all()
        )

        history.append({
            "id": session.id,
            "role": session.role,
            "experience_level": session.experience_level,
            "topic": session.topic,
            "created_at": session.created_at,
            "answers": [
                {
                    "id": answer.id,
                    "question": answer.question,
                    "answer": answer.answer,
                    "score": answer.score,
                    "feedback": answer.feedback,
                    "created_at": answer.created_at
                }
                for answer in answers
            ]
        })

    return history