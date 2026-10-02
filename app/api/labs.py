from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any
from .. import models, database, schemas
from ..security.auth import get_current_user
from ..services.engine import LabEngine
import json

router = APIRouter()

class TestPayload(BaseModel):
    payload: str = ""
    lab_id: str = ""

@router.get("/")
def get_labs(db: Session = Depends(database.get_db)):
    return db.query(models.Lab).all()

@router.get("/{lab_id}")
def get_lab(lab_id: str, db: Session = Depends(database.get_db)):
    lab = db.query(models.Lab).filter_by(id=lab_id).first()
    if not lab:
        raise HTTPException(status_code=404, detail="Lab not found")
    return lab

@router.get("/{lab_id}/hint")
def get_lab_hint(lab_id: str, db: Session = Depends(database.get_db)):
    # Standard placeholder hint for now
    return {"hint": f"Examine the constraints of the {lab_id} model and try to bypass them."}

@router.post("/attack")
def execute_lab_attack(request: TestPayload, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    lab_id = request.lab_id
    if not lab_id:
        raise HTTPException(status_code=400, detail="Missing lab_id")
        
    engine = LabEngine(db, current_user, lab_id)
    response, is_vuln, evidence, extra_data = engine.process_interaction(request.payload)
    
    return {
        "vulnerable": is_vuln,
        "evidence": evidence or response,
        "response": response,
        "extra_data": extra_data,
        "status": 200
    }

@router.get("/{lab_id}/history")
def get_lab_history(lab_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    attempts = db.query(models.LabAttempt).filter_by(user_id=current_user.id, lab_id=lab_id).order_by(models.LabAttempt.timestamp.desc()).all()
    return attempts

@router.get("/{lab_id}/progress")
def get_lab_progress(lab_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    prog = db.query(models.LabProgress).filter_by(user_id=current_user.id, lab_id=lab_id).first()
    if not prog:
        return {"attempts": 0, "completed": False, "objectives": {}}
    return {
        "attempts": prog.attempts,
        "completed": prog.completed,
        "objectives": json.loads(prog.objectives_json) if prog.objectives_json else {}
    }

@router.post("/{lab_id}/reset")
def reset_lab(lab_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    # Standard reset logic: just return success to clear frontend state,
    # optionally delete history if required by design.
    return {"status": "success", "message": "Lab reset"}
