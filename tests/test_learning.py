import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_learning_flow():
    # Login as admin to get token
    response = client.post("/api/auth/login", data={"username": "admin", "password": "admin"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 1. Get all learning modules
    response = client.get("/api/learning/", headers=headers)
    assert response.status_code == 200
    modules = response.json()
    assert len(modules) == 15
    assert modules[0]["id"] == "mod01"

    # 2. Get module details
    response = client.get("/api/learning/mod01", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["module"]["title"] == "AI Fundamentals"
    assert len(data["lessons"]) > 0

    # 3. Get lesson content
    lesson_id = data["lessons"][0]["id"]
    response = client.get(f"/api/learning/mod01/lessons/{lesson_id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["id"] == lesson_id

    # 4. Complete lesson
    response = client.post(f"/api/learning/mod01/lessons/{lesson_id}/complete", headers=headers)
    assert response.status_code == 200

    # 5. Take Quiz
    # Start attempt
    response = client.post("/api/learning/mod01/quiz/start", headers=headers)
    assert response.status_code == 200
    attempt_id = response.json()["attempt_id"]
    
    # Get attempt questions
    response = client.get(f"/api/learning/quiz/{attempt_id}", headers=headers)
    assert response.status_code == 200
    questions = response.json()["questions"]
    assert len(questions) >= 5
    
    # Check that there are no 'Sample question' in question text
    for q in questions:
        assert "Sample question" not in q["question"]
    
    # Submit correct quiz (answering mostly correctly)
    answers = {q["question_id"]: 0 for q in questions} # correct index is mostly 0 due to seeding
    
    response = client.post("/api/learning/quiz/submit", json={"attempt_id": attempt_id, "answers": answers}, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "score" in result
    assert result["passed"] is True
    
    # 6. Check Overall Progress
    response = client.get("/api/learning/progress", headers=headers)
    assert response.status_code == 200
    prog = response.json()
    assert prog["modules_total"] == 15

    # 7. Add Bookmark
    response = client.post("/api/learning/bookmarks", json={"lesson_id": lesson_id}, headers=headers)
    assert response.status_code == 200

    # 8. Add Note
    response = client.post("/api/learning/notes", json={"lesson_id": lesson_id, "content": "This is a note"}, headers=headers)
    assert response.status_code == 200

    # 9. Search
    response = client.get("/api/learning/search?q=AI", headers=headers)
    assert response.status_code == 200
    assert len(response.json()["modules"]) > 0
