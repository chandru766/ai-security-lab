from pydantic import BaseModel, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: str = "user"
    tenant: str = "tenantA"

class UserRead(UserBase):
    id: int
    role: str
    tenant: str
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class ChatRequest(BaseModel):
    message: str
    lab_id: Optional[str] = None
    
class ChatResponse(BaseModel):
    response: str
    events: List[Dict[str, Any]] = []

class LabRead(BaseModel):
    id: str
    number: int
    title: str
    description: str
    category: str
    difficulty: str
    estimated_time: str
    target: str
    model_config = ConfigDict(from_attributes=True)

class LabProgressRead(BaseModel):
    lab_id: str
    completed: bool
    attempts: int
    successful_attacks: int
    evidence: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

class SecurityEventRead(BaseModel):
    id: int
    timestamp: datetime
    username: str
    tenant: str
    attack_type: str
    payload: str
    request_data: str
    response_data: str
    result: str
    severity: str
    endpoint: str
    model_config = ConfigDict(from_attributes=True)

class ModeUpdate(BaseModel):
    mode: str

class QuizSubmit(BaseModel):
    attempt_id: int
    answers: Dict[int, int] # question_id -> option_index

class KnowledgeCheckAnswer(BaseModel):
    answer: int

class BookmarkCreate(BaseModel):
    lesson_id: str

class NoteCreate(BaseModel):
    lesson_id: str
    content: str

class ReportRead(BaseModel):
    id: int
    timestamp: datetime
    content: str
    model_config = ConfigDict(from_attributes=True)
