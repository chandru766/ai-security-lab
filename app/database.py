from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
import os
import shutil

# Check if running in Vercel Serverless environment
db_url = settings.DATABASE_URL
if os.environ.get("VERCEL"):
    tmp_db_path = "/tmp/ai_security_lab.db"
    src_db_path = os.path.join(os.getcwd(), "data", "ai_security_lab.db")
    
    # Copy read-only bundled DB to /tmp for read/write access
    if os.path.exists(src_db_path) and not os.path.exists(tmp_db_path):
        shutil.copy2(src_db_path, tmp_db_path)
    
    db_url = "sqlite:///" + tmp_db_path

db_dir = os.path.dirname(db_url.replace("sqlite:///", "").replace("./", ""))
if db_dir and not db_dir.startswith("/tmp"):
    os.makedirs(db_dir, exist_ok=True)

engine = create_engine(
    db_url, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
