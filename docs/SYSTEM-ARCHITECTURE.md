# System Architecture

## Overview
AI Security Lab is a monolithic Single-Page Application (SPA) backed by a FastAPI Python server. It employs a traditional n-tier architecture adjusted for a security simulation environment.

## High-Level Architecture Diagram
```mermaid
graph TD
    User([User])
    subscript_UI[Vanilla JS / HTML / CSS]
    
    subgraph Frontend [Browser Layer]
        subscript_UI
    end
    
    subgraph Backend [FastAPI Application]
        API_Routes[REST API Routes]
        
        subgraph Services [Application Services]
            Auth[Auth Engine]
            LabEng[Lab Engine]
            LearnEng[Learning Engine]
            QuizEng[Quiz Engine]
            ProgEng[Progress Engine]
            EventEng[Security Event Engine]
            RepEng[Report Engine]
        end
        
        MockLLM[Mock LLM / Target Engine]
    end
    
    subgraph Storage [Data Layer]
        DB[(SQLite / SQLAlchemy)]
    end
    
    User --> Frontend
    Frontend -->|JSON/REST| API_Routes
    API_Routes --> Auth
    API_Routes --> LabEng
    API_Routes --> LearnEng
    API_Routes --> QuizEng
    API_Routes --> ProgEng
    API_Routes --> EventEng
    API_Routes --> RepEng
    
    LabEng --> MockLLM
    
    Services --> DB
```

## Component Details
1. **Frontend**: Static files served by the backend or a CDN. Uses `app.js` to manage state globally (`window.LABS_CACHE`).
2. **Backend**: FastAPI running on Uvicorn. Uses Dependency Injection for Database sessions and Auth.
3. **Application Services**: Core logic located in `app/services/` separating API routing from business logic.
4. **Mock LLM**: Resides in `app/services/mock_llm.py` and `targets.py`. Processes inputs using regex and keyword logic to mimic LLM outputs safely.
5. **Data Layer**: SQLite database (`app/models/core.py`) tracking progress, users, events, and quiz attempts.\n