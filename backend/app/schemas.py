
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {"from_attributes": True}

from datetime import datetime
from pydantic import BaseModel, Field


class InterviewSessionCreate(BaseModel):
    role: str = Field(min_length=2, max_length=100)
    experience_level: str = Field(min_length=2, max_length=50)
    topic: str = Field(min_length=2, max_length=100)


class InterviewSessionResponse(BaseModel):
    id: int
    user_id: int
    role: str
    experience_level: str
    topic: str
    created_at: datetime

    model_config = {"from_attributes": True}

class InterviewAnswerCreate(BaseModel):
    session_id: int
    question: str = Field(min_length=1)
    answer: str = Field(min_length=1)


class InterviewAnswerResponse(BaseModel):
    id: int
    session_id: int
    question: str
    answer: str
    created_at: datetime

    model_config = {"from_attributes": True}