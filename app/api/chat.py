from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas
from ..security.auth import get_current_user
from ..services.engine import LabEngine

router = APIRouter()

@router.post("/")
def chat(request: schemas.ChatRequest, db: Session = Depends(database.get_db), current_user: models.User = Depends(get_current_user)):
    lab_id = request.lab_id
    if not lab_id:
        return {"response": "No lab selected", "events": []}
    
    engine = LabEngine(db, current_user, lab_id)
    response, is_vuln, evidence, extra_data = engine.process_interaction(request.message)
    
    events = []
    if is_vuln:
        events.append({"type": "Vulnerability Found", "evidence": evidence})
        
    return {"response": response, "events": events, "extra_data": extra_data, "vulnerable": is_vuln}
