from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from sqlalchemy.sql import func
from typing import List, Dict, Any
from .. import models, database, schemas
from ..security.auth import get_current_user
import json

router = APIRouter()

@router.get("/")
def get_modules(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    modules = db.query(models.LearningModule).all()
    # Attach progress
    result = []
    for mod in modules:
        lessons_count = db.query(models.LearningLesson).filter_by(module_id=mod.id).count()
        completed_lessons = db.query(models.LessonProgress).join(models.LearningLesson).filter(
            models.LearningLesson.module_id == mod.id, 
            models.LessonProgress.user_id == current_user.id,
            models.LessonProgress.completed == True
        ).count()
        
        quiz_attempt = db.query(models.QuizAttempt).filter_by(user_id=current_user.id, module_id=mod.id).order_by(models.QuizAttempt.score.desc()).first()
        
        result.append({
            "id": mod.id,
            "title": mod.title,
            "description": mod.description,
            "difficulty": mod.difficulty,
            "estimated_time": mod.estimated_time,
            "prerequisites": json.loads(mod.prerequisites),
            "related_labs": json.loads(mod.related_labs),
            "lessons_total": lessons_count,
            "lessons_completed": completed_lessons,
            "quiz_score": quiz_attempt.score if quiz_attempt else None,
            "completed": (completed_lessons == lessons_count and lessons_count > 0 and quiz_attempt and quiz_attempt.passed)
        })
    return result

@router.get("/search")
def search_learning(q: str = Query(...), db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    search_term = f"%{q}%"
    modules = db.query(models.LearningModule).filter(
        or_(models.LearningModule.title.ilike(search_term), models.LearningModule.description.ilike(search_term))
    ).all()
    
    lessons = db.query(models.LearningLesson).filter(
        or_(models.LearningLesson.title.ilike(search_term), models.LearningLesson.content.ilike(search_term))
    ).all()
    
    return {
        "modules": [{"id": m.id, "title": m.title} for m in modules],
        "lessons": [{"id": l.id, "module_id": l.module_id, "title": l.title} for l in lessons]
    }

@router.get("/progress")
def get_overall_progress(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    modules = db.query(models.LearningModule).all()
    completed_modules = 0
    for mod in modules:
        lessons_count = db.query(models.LearningLesson).filter_by(module_id=mod.id).count()
        completed_lessons = db.query(models.LessonProgress).join(models.LearningLesson).filter(
            models.LearningLesson.module_id == mod.id, 
            models.LessonProgress.user_id == current_user.id,
            models.LessonProgress.completed == True
        ).count()
        quiz_attempt = db.query(models.QuizAttempt).filter_by(user_id=current_user.id, module_id=mod.id).order_by(models.QuizAttempt.score.desc()).first()
        if completed_lessons == lessons_count and lessons_count > 0 and quiz_attempt and quiz_attempt.passed:
            completed_modules += 1
            
    total_lessons = db.query(models.LearningLesson).count()
    completed_lessons = db.query(models.LessonProgress).filter_by(user_id=current_user.id, completed=True).count()
    
    quiz_attempts = db.query(models.QuizAttempt).filter_by(user_id=current_user.id).all()
    quiz_avg = sum(a.score for a in quiz_attempts) / len(quiz_attempts) if quiz_attempts else 0
    
    return {
        "modules_total": len(modules),
        "modules_completed": completed_modules,
        "lessons_total": total_lessons,
        "lessons_completed": completed_lessons,
        "quiz_average": round(quiz_avg, 2)
    }

@router.get("/{module_id}")
def get_module(module_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    mod = db.query(models.LearningModule).filter_by(id=module_id).first()
    if not mod:
        raise HTTPException(status_code=404)
    lessons = db.query(models.LearningLesson).filter_by(module_id=module_id).order_by(models.LearningLesson.order).all()
    
    # Progress map
    progress_records = db.query(models.LessonProgress).filter_by(user_id=current_user.id).all()
    completed_lesson_ids = [p.lesson_id for p in progress_records if p.completed]
    
    return {
        "module": {
            "id": mod.id,
            "title": mod.title,
            "description": mod.description,
            "related_labs": json.loads(mod.related_labs)
        },
        "lessons": [
            {"id": l.id, "title": l.title, "completed": l.id in completed_lesson_ids} for l in lessons
        ]
    }

@router.get("/{module_id}/lessons/{lesson_id}")
def get_lesson(module_id: str, lesson_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    lesson = db.query(models.LearningLesson).filter_by(id=lesson_id, module_id=module_id).first()
    if not lesson:
        raise HTTPException(status_code=404)
    kcs = db.query(models.KnowledgeCheck).filter_by(lesson_id=lesson_id).all()
    
    return {
        "id": lesson.id,
        "title": lesson.title,
        "content": lesson.content,
        "knowledge_checks": [
            {"id": kc.id, "question": kc.question, "options": json.loads(kc.options)} for kc in kcs
        ]
    }

@router.post("/{module_id}/lessons/{lesson_id}/complete")
def complete_lesson(module_id: str, lesson_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    prog = db.query(models.LessonProgress).filter_by(user_id=current_user.id, lesson_id=lesson_id).first()
    if not prog:
        prog = models.LessonProgress(user_id=current_user.id, lesson_id=lesson_id, completed=True)
        db.add(prog)
    else:
        prog.completed = True
    db.commit()
    return {"status": "success"}

@router.post("/{module_id}/knowledge-check")
def submit_knowledge_check(module_id: str, request: schemas.KnowledgeCheckAnswer, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # simplified mock for API interface
    return {"status": "success"}

@router.post("/{module_id}/quiz/start")
def start_quiz(module_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    questions = db.query(models.QuizQuestion).filter_by(module_id=module_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this module")
        
    import random
    random.shuffle(questions)
    
    attempt = models.QuizAttempt(user_id=current_user.id, module_id=module_id, total_questions=len(questions))
    db.add(attempt)
    db.commit()
    db.refresh(attempt)
    
    for idx, q in enumerate(questions):
        aq = models.QuizAttemptQuestion(attempt_id=attempt.id, question_id=q.id, order_index=idx)
        db.add(aq)
    db.commit()
    
    return {"attempt_id": attempt.id}

@router.get("/quiz/{attempt_id}")
def get_quiz_attempt(attempt_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    attempt = db.query(models.QuizAttempt).filter_by(id=attempt_id, user_id=current_user.id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
        
    aqs = db.query(models.QuizAttemptQuestion).filter_by(attempt_id=attempt_id).order_by(models.QuizAttemptQuestion.order_index).all()
    
    result = []
    for aq in aqs:
        q = db.query(models.QuizQuestion).filter_by(id=aq.question_id).first()
        result.append({
            "question_id": q.id,
            "question": q.question,
            "options": json.loads(q.options)
        })
        
    return {"attempt_id": attempt.id, "module_id": attempt.module_id, "questions": result}

@router.post("/quiz/submit")
def submit_quiz(request: schemas.QuizSubmit, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    attempt = db.query(models.QuizAttempt).filter_by(id=request.attempt_id, user_id=current_user.id).first()
    if not attempt or attempt.completed:
        raise HTTPException(status_code=400, detail="Invalid attempt or already completed")
        
    aqs = db.query(models.QuizAttemptQuestion).filter_by(attempt_id=attempt.id).all()
    
    correct_count = 0
    results = []
    for aq in aqs:
        q = db.query(models.QuizQuestion).filter_by(id=aq.question_id).first()
        user_ans = request.answers.get(str(q.id)) or request.answers.get(q.id)
        
        if user_ans is not None:
            user_ans = int(user_ans)
            aq.user_answer = user_ans
            
        is_correct = (user_ans == q.correct_index)
        if is_correct:
            correct_count += 1
            
        results.append({
            "question_id": q.id,
            "question": q.question,
            "user_answer": user_ans,
            "correct_index": q.correct_index,
            "is_correct": is_correct,
            "explanation": q.explanation
        })
        
    score = (correct_count / len(aqs)) * 100 if aqs else 0
    passed = score >= 80.0
    
    attempt.score = score
    attempt.passed = passed
    attempt.completed = True
    attempt.completed_at = func.now()
    db.commit()
    
    return {"score": score, "passed": passed, "results": results}

# Bookmarks
@router.get("/bookmarks")
def get_bookmarks(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    bms = db.query(models.Bookmark).filter_by(user_id=current_user.id).all()
    res = []
    for bm in bms:
        les = db.query(models.LearningLesson).filter_by(id=bm.lesson_id).first()
        if les:
            res.append({"id": bm.id, "lesson_id": les.id, "title": les.title})
    return res

@router.post("/bookmarks")
def add_bookmark(request: schemas.BookmarkCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    bm = models.Bookmark(user_id=current_user.id, lesson_id=request.lesson_id)
    db.add(bm)
    db.commit()
    return {"status": "success", "id": bm.id}

# Notes
@router.get("/notes")
def get_notes(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    notes = db.query(models.LearningNote).filter_by(user_id=current_user.id).all()
    return [{"id": n.id, "lesson_id": n.lesson_id, "content": n.content} for n in notes]

@router.post("/notes")
def add_note(request: schemas.NoteCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    note = models.LearningNote(user_id=current_user.id, lesson_id=request.lesson_id, content=request.content)
    db.add(note)
    db.commit()
    return {"status": "success", "id": note.id}
