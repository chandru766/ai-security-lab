from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
import json
from .. import models, schemas, database
from ..security.auth import get_current_user

router = APIRouter()

@router.get("/mode")
def get_mode(db: Session = Depends(database.get_db)):
    state = db.query(models.GlobalState).first()
    if not state:
        state = models.GlobalState(security_mode="VULNERABLE")
        db.add(state)
        db.commit()
    return {"mode": state.security_mode}

@router.post("/mode")
def set_mode(request: schemas.ModeUpdate, db: Session = Depends(database.get_db)):
    state = db.query(models.GlobalState).first()
    if not state:
        state = models.GlobalState(security_mode=request.mode)
        db.add(state)
    else:
        state.security_mode = request.mode
    db.commit()
    return {"mode": state.security_mode}

@router.get("/events", response_model=List[schemas.SecurityEventRead])
def get_events(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.SecurityEvent).order_by(models.SecurityEvent.timestamp.desc()).limit(50).all()

@router.get("/progress", response_model=List[schemas.LabProgressRead])
def get_progress(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.LabProgress).filter(models.LabProgress.user_id == current_user.id).all()

@router.get("/report")
def get_report(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    events = db.query(models.SecurityEvent).count()
    vulnerable_events = db.query(models.SecurityEvent).filter(models.SecurityEvent.result == "Vulnerable").count()
    return {
        "title": "AI Security Lab Assessment Report",
        "total_events_logged": events,
        "vulnerabilities_exploited": vulnerable_events,
        "recommendation": "Implement mitigations outlined in the lab exercises."
    }

@router.get("/health")
def get_health():
    return {
        "status": "online",
        "services": {
            "ai_models": "ONLINE",
            "lab_environment": "ONLINE",
            "database": "ONLINE",
            "security_monitoring": "ONLINE",
            "event_logging": "ONLINE",
            "learning_engine": "ONLINE"
        }
    }

@router.get("/dashboard")
def get_dashboard(db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Calculate finding counts by category
    findings = db.query(models.SecurityEvent.attack_type, models.func.count(models.SecurityEvent.id)).group_by(models.SecurityEvent.attack_type).all()
    threat_overview = {f[0]: f[1] for f in findings}
    
    # Recent findings
    recent_findings = db.query(models.SecurityEvent).filter(models.SecurityEvent.result == "Vulnerable").order_by(models.SecurityEvent.timestamp.desc()).limit(5).all()
    findings_list = [{"severity": e.severity, "finding": e.attack_type, "lab": e.endpoint, "status": "OPEN", "time": e.timestamp.isoformat() if e.timestamp else ""} for e in recent_findings]
    
    # Recent Activity (mix of events and progress)
    recent_events = db.query(models.SecurityEvent).order_by(models.SecurityEvent.timestamp.desc()).limit(5).all()
    activity = []
    for e in recent_events:
        activity.append({
            "type": "FINDING" if e.result == "Vulnerable" else "EVENT",
            "desc": f"{e.attack_type} detected in {e.endpoint}",
            "time": e.timestamp.isoformat() if e.timestamp else ""
        })
    
    return {
        "threat_overview": threat_overview,
        "recent_findings": findings_list,
        "recent_activity": activity
    }
