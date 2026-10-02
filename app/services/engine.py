from sqlalchemy.orm import Session
from datetime import datetime
from .. import models
from .targets import TARGET_MAP
import json

class LabEngine:
    def __init__(self, db: Session, user: models.User, lab_id: str):
        self.db = db
        self.user = user
        self.lab_id = lab_id
        
        state = self.db.query(models.GlobalState).first()
        self.is_secure = state.security_mode == "SECURE" if state else False

    def _log_event(self, attack_type, payload, request_data, response_data, result, severity, evidence):
        event = models.SecurityEvent(
            username=self.user.username,
            tenant=self.user.tenant,
            attack_type=attack_type,
            payload=payload,
            request_data=json.dumps(request_data),
            response_data=json.dumps(response_data),
            result=result,
            severity=severity,
            endpoint=f"/api/labs/{self.lab_id}"
        )
        self.db.add(event)
        
        # Log attack attempt history
        attempt = models.LabAttempt(
            user_id=self.user.id,
            lab_id=self.lab_id,
            payload=payload,
            mode="SECURE" if self.is_secure else "VULNERABLE",
            result=result,
            evidence=evidence
        )
        self.db.add(attempt)
        self.db.commit()

    def process_interaction(self, payload: str):
        target_cls = TARGET_MAP.get(self.lab_id)
        if not target_cls:
            raise ValueError("Lab target not found")
            
        target = target_cls(is_secure=self.is_secure, db=self.db, user=self.user)
        response, is_vuln, evidence, extra_data = target.process(payload)
        
        # Ensure progress record exists
        prog = self.db.query(models.LabProgress).filter_by(user_id=self.user.id, lab_id=self.lab_id).first()
        if not prog:
            default_objs = {
                "Understand Target": True,
                "Execute Attack": False,
                "Capture Evidence": False,
                "Retest Secure Configuration": False
            }
            prog = models.LabProgress(
                user_id=self.user.id, 
                lab_id=self.lab_id, 
                attempts=0, 
                successful_attacks=0,
                objectives_json=json.dumps(default_objs)
            )
            self.db.add(prog)
            
        prog.attempts += 1
        
        result_str = "Vulnerable" if is_vuln else "Safe/Blocked"
        severity = "HIGH" if is_vuln else "LOW"
        
        self._log_event(
            attack_type=self.lab_id,
            payload=payload,
            request_data={"message": payload},
            response_data={"response": response, "extra": extra_data},
            result=result_str,
            severity=severity,
            evidence=evidence
        )
        
        # Update completion conditions (Objectives)
        if is_vuln:
            prog.successful_attacks += 1
            prog.evidence = evidence
            # Mark objectives complete (Mock logic)
            if prog.objectives_json:
                objs = json.loads(prog.objectives_json)
                objs["Execute Attack"] = True
                objs["Capture Evidence"] = True
                prog.objectives_json = json.dumps(objs)
        elif self.is_secure and prog.successful_attacks > 0 and evidence:
            # If they are in secure mode, and blocked an attack they previously succeeded on
            if prog.objectives_json:
                objs = json.loads(prog.objectives_json)
                objs["Retest Secure Configuration"] = True
                prog.objectives_json = json.dumps(objs)
                # If all objectives met, complete lab
                if all(objs.values()):
                    prog.completed = True

        self.db.commit()
        return response, is_vuln, evidence, extra_data
