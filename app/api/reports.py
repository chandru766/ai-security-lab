from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, database, schemas
from ..security.auth import get_current_user
import json
from typing import List

router = APIRouter()

@router.get("/", response_model=List[schemas.ReportRead])
def get_reports(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.Report).filter(models.Report.user_id == current_user.id).all()

@router.post("/generate")
def generate_report(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    events = db.query(models.SecurityEvent).filter(models.SecurityEvent.username == current_user.username).count()
    completed_labs = db.query(models.LabProgress).filter(models.LabProgress.user_id == current_user.id, models.LabProgress.completed == True).count()
    
    report_data = {
        "title": "AI Security Assessment Report",
        "tester": current_user.username,
        "labs_completed": completed_labs,
        "security_events_logged": events,
        "findings": "Multiple vulnerabilities identified in AI targets including Prompt Injection, RAG Poisoning, and Access Control.",
        "recommendations": "Implement robust prompt boundaries, RAG context validation, and strict tool authorization policies."
    }
    
    report = models.Report(user_id=current_user.id, content=json.dumps(report_data))
    db.add(report)
    db.commit()
    
    return {"id": report.id, "content": report_data}
