import sys
import os

print("[PASS] Python version:", sys.version.split(" ")[0])

try:
    import fastapi
    print("[PASS] FastAPI")
except ImportError:
    print("[FAIL] FastAPI missing")

try:
    import uvicorn
    print("[PASS] Uvicorn")
except ImportError:
    print("[FAIL] Uvicorn missing")

if os.path.exists("data/ai_security_lab.db"):
    print("[PASS] Database exists")
else:
    print("[WARN] Database not initialized yet")

print("[PASS] All diagnostics complete.")
