from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, SessionLocal
from .api import auth_router, chat_router, labs_router, system_router, learning_router, reports_router
from . import models
from .security.auth import get_password_hash
import os
import json

Base.metadata.create_all(bind=engine)

LABS = [
    {"id": "lab01", "number": 1, "title": "Direct Prompt Injection", "description": "Bypass instructions to reveal a secret.", "category": "LLM Security", "difficulty": "Easy", "estimated_time": "15 min", "target": "Customer Support AI"},
    {"id": "lab02", "number": 2, "title": "System Prompt Extraction", "description": "Extract hidden instructions.", "category": "LLM Security", "difficulty": "Easy", "estimated_time": "15 min", "target": "AI Agent"},
    {"id": "lab03", "number": 3, "title": "Jailbreak Testing", "description": "Bypass safety guidelines.", "category": "LLM Security", "difficulty": "Medium", "estimated_time": "20 min", "target": "Safe AI"},
    {"id": "lab04", "number": 4, "title": "Sensitive Information Disclosure", "description": "Force model to leak synthetic confidential data.", "category": "LLM Security", "difficulty": "Easy", "estimated_time": "15 min", "target": "HR AI"},
    {"id": "lab05", "number": 5, "title": "RAG Security", "description": "Bypass RAG access controls.", "category": "RAG Security", "difficulty": "Medium", "estimated_time": "20 min", "target": "Internal Knowledge Assistant"},
    {"id": "lab06", "number": 6, "title": "RAG Poisoning", "description": "Poison the retrieval context.", "category": "RAG Security", "difficulty": "Hard", "estimated_time": "30 min", "target": "Knowledge Agent"},
    {"id": "lab07", "number": 7, "title": "Indirect Prompt Injection", "description": "Inject commands via retrieved docs.", "category": "RAG Security", "difficulty": "Hard", "estimated_time": "30 min", "target": "Document Summarizer"},
    {"id": "lab08", "number": 8, "title": "Insecure Output Handling", "description": "Exploit lack of output sanitization (XSS).", "category": "App Security", "difficulty": "Medium", "estimated_time": "20 min", "target": "Web Generator AI"},
    {"id": "lab09", "number": 9, "title": "Excessive Agency", "description": "Execute unauthorized tools.", "category": "Agent Security", "difficulty": "Medium", "estimated_time": "25 min", "target": "Admin Agent"},
    {"id": "lab10", "number": 10, "title": "AI Agent Tool Abuse", "description": "Inject commands into tool parameters.", "category": "Agent Security", "difficulty": "Hard", "estimated_time": "30 min", "target": "DevOps Agent"},
    {"id": "lab11", "number": 11, "title": "Broken Access Control", "description": "Cross-tenant data access.", "category": "Auth Security", "difficulty": "Medium", "estimated_time": "20 min", "target": "Multi-Tenant AI"},
    {"id": "lab12", "number": 12, "title": "Cross-Tenant AI Data Access", "description": "Leak context from another tenant.", "category": "Auth Security", "difficulty": "Medium", "estimated_time": "20 min", "target": "Multi-Tenant Assistant"},
    {"id": "lab13", "number": 13, "title": "AI Supply Chain Security", "description": "Load untrusted model component.", "category": "Supply Chain", "difficulty": "Hard", "estimated_time": "30 min", "target": "Model Registry"},
    {"id": "lab14", "number": 14, "title": "Model/Prompt Configuration Security", "description": "Exploit unsafe model configuration.", "category": "App Security", "difficulty": "Easy", "estimated_time": "15 min", "target": "AI Configuration Console"},
    {"id": "lab15", "number": 15, "title": "AI Security Assessment", "description": "Complete final assessment.", "category": "Assessment", "difficulty": "Expert", "estimated_time": "60 min", "target": "Enterprise AI"}
]

from .seed_learning import seed_learning_content

def init_db():
    db = SessionLocal()
    if db.query(models.User).count() == 0:
        db.add_all([
            models.User(username="admin", hashed_password=get_password_hash("admin"), role="admin", tenant="tenantA"),
            models.User(username="tenantb", hashed_password=get_password_hash("tenantb"), role="user", tenant="tenantB"),
        ])
    if db.query(models.GlobalState).count() == 0:
        db.add(models.GlobalState(security_mode="VULNERABLE"))
    
    if db.query(models.Lab).count() == 0:
        for l in LABS:
            db.add(models.Lab(**l))
            
    seed_learning_content(db)
    
    db.commit()
    db.close()

init_db()

app = FastAPI(title="AI Security Lab V2")

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])
app.include_router(labs_router, prefix="/api/labs", tags=["labs"])
app.include_router(system_router, prefix="/api/system", tags=["system"])
app.include_router(learning_router, prefix="/api/learning", tags=["learning"])
app.include_router(reports_router, prefix="/api/reports", tags=["reports"])

@app.get("/health")
def health():
    return {"status": "ok"}

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
os.makedirs(frontend_dir, exist_ok=True)
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
