@echo off
echo Starting AI Security Lab V2...
python -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
python diagnose.py
python -m pytest -q
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
