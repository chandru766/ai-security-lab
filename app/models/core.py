from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")
    tenant = Column(String, default="tenantA")
    progress = relationship("LabProgress", back_populates="user")
    learning_progress = relationship("LearningProgress", back_populates="user")

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    username = Column(String)
    tenant = Column(String)
    attack_type = Column(String)
    payload = Column(Text)
    request_data = Column(Text)
    response_data = Column(Text)
    result = Column(String)
    severity = Column(String)
    endpoint = Column(String)

class Lab(Base):
    __tablename__ = "labs"
    id = Column(String, primary_key=True, index=True) # lab01, lab02...
    number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    category = Column(String)
    difficulty = Column(String)
    estimated_time = Column(String)
    target = Column(String)

class LabProgress(Base):
    __tablename__ = "lab_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lab_id = Column(String, ForeignKey("labs.id"))
    completed = Column(Boolean, default=False)
    attempts = Column(Integer, default=0)
    successful_attacks = Column(Integer, default=0)
    evidence = Column(Text, nullable=True)
    objectives_json = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="progress")

class LabAttempt(Base):
    __tablename__ = "lab_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lab_id = Column(String, ForeignKey("labs.id"))
    payload = Column(Text)
    mode = Column(String)
    result = Column(String)
    evidence = Column(Text, nullable=True)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class LearningModule(Base):
    __tablename__ = "learning_modules"
    id = Column(String, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text, default="")
    difficulty = Column(String, default="Beginner")
    estimated_time = Column(String, default="15 minutes")
    prerequisites = Column(Text, default="[]") # JSON list of module IDs
    related_labs = Column(Text, default="[]") # JSON list of lab IDs

class LearningLesson(Base):
    __tablename__ = "learning_lessons"
    id = Column(String, primary_key=True, index=True)
    module_id = Column(String, ForeignKey("learning_modules.id"))
    title = Column(String)
    content = Column(Text)
    order = Column(Integer)

class LessonProgress(Base):
    __tablename__ = "lesson_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(String, ForeignKey("learning_lessons.id"))
    completed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class KnowledgeCheck(Base):
    __tablename__ = "knowledge_checks"
    id = Column(Integer, primary_key=True, index=True)
    lesson_id = Column(String, ForeignKey("learning_lessons.id"))
    question = Column(String)
    options = Column(Text) # JSON string
    correct_index = Column(Integer)
    explanation = Column(Text)

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(String, ForeignKey("learning_lessons.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class LearningNote(Base):
    __tablename__ = "learning_notes"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    lesson_id = Column(String, ForeignKey("learning_lessons.id"))
    content = Column(Text)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

class QuizQuestion(Base):
    __tablename__ = "quiz_questions"
    id = Column(Integer, primary_key=True, index=True)
    module_id = Column(String, ForeignKey("learning_modules.id"))
    question = Column(String)
    options = Column(Text) # JSON string ["A", "B", "C", "D"]
    correct_index = Column(Integer)
    explanation = Column(Text)

class LearningProgress(Base):
    __tablename__ = "learning_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    module_id = Column(String, ForeignKey("learning_modules.id"))
    completed = Column(Boolean, default=False)
    score = Column(Float, default=0.0)
    user = relationship("User", back_populates="learning_progress")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    module_id = Column(String, ForeignKey("learning_modules.id"))
    score = Column(Float, default=0.0)
    passed = Column(Boolean, default=False)
    total_questions = Column(Integer, default=0)
    completed = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

class QuizAttemptQuestion(Base):
    __tablename__ = "quiz_attempt_questions"
    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"))
    question_id = Column(Integer, ForeignKey("quiz_questions.id"))
    order_index = Column(Integer)
    user_answer = Column(Integer, nullable=True)

class Report(Base):
    __tablename__ = "reports"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    content = Column(Text) # JSON report

class GlobalState(Base):
    __tablename__ = "global_state"
    id = Column(Integer, primary_key=True, index=True)
    security_mode = Column(String, default="VULNERABLE")
