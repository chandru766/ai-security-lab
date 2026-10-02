# Deployment (Local)

## Prerequisites
- Python 3.10+
- `pip`

## Instructions
1. **Virtual Environment**:
   ```bash
   python -m venv venv
   .env\Scriptsctivate
   ```
2. **Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Initialization**:
   ```bash
   python scripts/seed.py
   python scripts/seed_learning.py
   ```
4. **Run Server**:
   ```bash
   .\start.bat
   # or
   uvicorn app.main:app --reload
   ```\n