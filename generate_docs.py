import os

def create_docs():
    docs_dir = "docs"
    diagrams_dir = os.path.join(docs_dir, "diagrams")
    
    os.makedirs(docs_dir, exist_ok=True)
    os.makedirs(diagrams_dir, exist_ok=True)
    
    files = {}
    
    files["README.md"] = """# 🔐 AI Security Lab

A hands-on AI Security & AI Red Teaming training platform designed to teach developers, security researchers, and engineers how to secure LLMs and AI applications.

## Overview
AI Security Lab is an educational and controlled security testing environment. It features a complete Learning Academy with 15 modules, a gamified penetration testing console with 15 hands-on labs, and a built-in mock LLM engine that responds dynamically to vulnerabilities without risking real-world data or costs.

## Key Features
- **Hands-On Lab Engine**: 15 custom-built labs covering OWASP LLM top 10 vulnerabilities.
- **AI Academy**: 15 comprehensive learning modules mapping concepts from fundamentals to advanced AI Red Teaming.
- **Mock LLM Target**: An in-memory evaluation engine providing deterministic yet dynamic responses to payloads.
- **Progress & Tracking**: Detailed event logging (SIEM-style), automated progress tracking, and report generation.
- **Gamified Experience**: Professional cybersecurity UI with Secure/Vulnerable toggle modes.

## Architecture
![System Architecture](diagrams/system-architecture.mmd)

## Technology Stack
- **Frontend**: Vanilla HTML / CSS / JavaScript (No bulky frameworks)
- **Backend**: Python / FastAPI
- **Database**: SQLite (local dev)
- **AI**: Custom Python Mock LLM Engine (Pattern & NLP based)
- **Security**: JWT Authentication, RBAC, Request logging
- **Deployment**: Vercel / Docker

## Project Structure
```
ai-security-lab/
├── app/                  # FastAPI Backend
│   ├── api/              # Route Handlers
│   ├── models/           # SQLAlchemy Models
│   ├── security/         # Auth & RBAC
│   └── services/         # Core Business Logic (Engine, LLM, Targets)
├── frontend/             # Single Page Application
├── tests/                # Pytest Test Suite
└── docs/                 # Platform Documentation
```

## Documentation Index
| Document | Description |
|---|---|
| [System Architecture](SYSTEM-ARCHITECTURE.md) | Platform architecture |
| [System Flow](SYSTEM-FLOW.md) | End-to-end application flow |
| [Lab Engine](LAB-ENGINE.md) | Lab execution architecture |
| [AI Security Flows](AI-SECURITY-FLOWS.md) | AI attack/security flows |
| [Learning Engine](LEARNING-ENGINE.md) | Learning platform |
| [Quiz System](QUIZ-SYSTEM.md) | Quiz architecture |
| [Progress Tracking](PROGRESS-TRACKING.md) | Progress system |
| [Database Design](DATABASE-DESIGN.md) | Database schema |
| [API Documentation](API-DOCUMENTATION.md) | API reference |
| [Authentication](AUTHENTICATION-AUTHORIZATION.md) | Auth and RBAC |
| [Security Design](SECURITY-DESIGN.md) | Security controls |
| [Evidence & Reporting](EVIDENCE-AND-REPORTING.md) | Evidence/report pipeline |
| [Monitoring](MONITORING-AND-EVENTS.md) | Security events |
| [Testing](TESTING.md) | Test strategy |
| [Deployment](DEPLOYMENT.md) | Local deployment |
| [Vercel Deployment](VERCEL-DEPLOYMENT.md) | Production deployment |
| [15 Labs](15-LABS.md) | Lab documentation |
| [Contributing](CONTRIBUTING.md) | Contribution guide |

## Security Notice
⚠ **EDUCATIONAL ENVIRONMENT**
All labs are designed for authorized, local security training and use synthetic data. Do not execute these attacks against systems you do not have permission to test.

## Author
Created & Developed by:
**Chandrasekar L**
Cybersecurity | AI Security | AI Red Teaming
"""

    files["SYSTEM-ARCHITECTURE.md"] = """# System Architecture

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
5. **Data Layer**: SQLite database (`app/models/core.py`) tracking progress, users, events, and quiz attempts.
"""

    files["SYSTEM-FLOW.md"] = """# System Flow

## User Journey
```mermaid
flowchart TD
    A[User] --> B[Login]
    B --> C{Dashboard}
    
    C -->|Selects Lab| D[Lab Detail]
    D --> E[Read Objective]
    E --> F[Send Attack Payload]
    F --> G[Lab Engine]
    G --> H[Mock Target Evaluation]
    H --> I{Vulnerability Detected?}
    I -->|Yes| J[Capture Evidence]
    I -->|No| K[Return Standard Response]
    J --> L[Update Progress]
    J --> M[Log Security Event]
    L --> N[Generate Final Report]
```

## Core Request Sequence
```mermaid
sequenceDiagram
    participant B as Browser
    participant A as API (FastAPI)
    participant LE as Lab Engine
    participant T as Target/MockLLM
    participant DB as Database
    
    B->>A: POST /api/labs/attack (Payload)
    A->>LE: process_interaction(payload)
    LE->>T: evaluate(payload)
    T-->>LE: is_vuln, response, evidence
    LE->>DB: create(LabAttempt)
    LE->>DB: create(SecurityEvent)
    DB-->>LE: OK
    LE-->>A: Evaluation Result
    A-->>B: JSON Response
```
"""

    files["LAB-ENGINE.md"] = """# Lab Engine

## Overview
The Lab Engine (`app/services/engine.py` and `app/services/targets.py`) is responsible for orchestrating the execution of penetration testing simulations.

## How Labs Work
- **Definition**: Labs are seeded into the database via `seed.py`.
- **Targets**: Each lab corresponds to a Target class mapping in `app/services/targets.py` (e.g., `TargetPromptInjection`, `TargetRAGPoisoning`).
- **Evaluation**: The target evaluates the user's string payload. It checks against expected adversarial patterns.
- **Modes**: 
  - `VULNERABLE`: The engine executes the attack successfully if the payload matches patterns.
  - `SECURE`: The engine blocks the attack regardless, demonstrating proper mitigation.

## Lab Execution Flow
```mermaid
flowchart TD
    A[User Input Payload] --> B[Lab Engine]
    B --> C{Check System Mode}
    C -->|Secure| D[Target - Apply Mitigations]
    C -->|Vulnerable| E[Target - Unfiltered Evaluation]
    
    D --> F[Blocked/Ineffective]
    E --> G{Contains Attack Pattern?}
    G -->|Yes| H[Vulnerable Output & Evidence]
    G -->|No| I[Standard Safe Output]
```
"""

    files["AI-SECURITY-FLOWS.md"] = """# AI Security Flows

These diagrams reflect the actual security concepts tested in the application's mock LLM engine.

## 1. Prompt Injection Flow
```mermaid
flowchart TD
    A[User Input] --> B[System Prompt Wrapper]
    B --> C[LLM Evaluation]
    C --> D{Instruction Override Detected?}
    D -->|Yes| E[Unexpected Action Executed]
    D -->|No| F[Normal Response]
```

## 2. RAG Poisoning Flow
```mermaid
flowchart TD
    A[Malicious Document] --> B[Knowledge Base]
    C[User Query] --> D[Retriever]
    D --> B
    D --> E[Retrieve Poisoned Context]
    E --> F[LLM Generation]
    F --> G[Manipulated Output Provided to User]
```

## 3. Excessive Agency Flow
```mermaid
flowchart TD
    A[User Prompt] --> B[AI Agent]
    B --> C{Permission Check?}
    C -->|Missing / Flawed| D[Execute Highly Privileged Tool]
    C -->|Proper| E[Access Denied]
    D --> F[Data Exfiltration / Modification]
```
"""

    files["LEARNING-ENGINE.md"] = """# Learning Engine

## Overview
The Learning Engine (`app/api/learning.py`) provides structured educational content for users before they attempt labs.

## Architecture
- **Modules**: High-level topics (e.g., "LLM Security").
- **Lessons**: Detailed reading material stored as HTML/Markdown in the database.
- **Quizzes**: End-of-module assessments verifying knowledge.
- **Progress Tracking**: Automatic tracking of completed modules and quiz scores.

## Learning Journey Flow
```mermaid
flowchart TD
    A[Start Module] --> B[Read Lessons]
    B --> C[Mark Lessons Complete]
    C --> D[Take Module Quiz]
    D --> E{Pass >= 70%?}
    E -->|Yes| F[Module Completed]
    E -->|No| G[Retry Quiz]
    F --> H[Unlock Related Labs]
```
"""

    files["QUIZ-SYSTEM.md"] = """# Quiz System

## Overview
The quiz system provides a server-side validated assessment environment to test user comprehension.

## Features
- **Server-Side Validation**: Answers are not exposed in the frontend.
- **Attempt Tracking**: `QuizAttempt` and `QuizAttemptQuestion` models track user history.
- **Explanation Feedback**: The backend returns explanations for correct/incorrect answers upon submission.

## Flow
```mermaid
sequenceDiagram
    participant User
    participant Front as Frontend
    participant API
    participant DB
    
    User->>Front: Start Quiz
    Front->>API: POST /api/learning/{mod}/quiz/start
    API->>DB: Create QuizAttempt
    API-->>Front: Return Question IDs & Text
    User->>Front: Submits Answers
    Front->>API: POST /api/learning/quiz/submit
    API->>DB: Evaluate & Update QuizAttempt
    API-->>Front: Score & Explanations
```
"""

    files["PROGRESS-TRACKING.md"] = """# Progress Tracking

## Overview
Progress is tracked across both Labs and Learning Modules, creating a unified `SystemProgress` overview.

## Models
- `LabProgress`: Tracks `attempts`, `completed` boolean, and `objectives_json`.
- `ModuleProgress`: Tracks which lessons are finished and overall module status.

## Flow
```mermaid
flowchart TD
    A[User Action] --> B{Action Type}
    B -->|Submit Quiz| C[Update ModuleProgress]
    B -->|Exploit Vulnerability| D[Update LabProgress]
    C --> E[Global Progress Engine]
    D --> E
    E --> F[Dashboard Statistics Updated]
```
"""

    files["DATABASE-DESIGN.md"] = """# Database Design

## Overview
The platform uses SQLAlchemy mapped to SQLite (local) or potentially PostgreSQL (production).

## ER Diagram
```mermaid
erDiagram
    User ||--o{ SecurityEvent : triggers
    User ||--o{ LabProgress : tracks
    User ||--o{ LabAttempt : creates
    User ||--o{ QuizAttempt : creates
    
    Lab ||--o{ LabProgress : has
    Lab ||--o{ LabAttempt : has
    
    LearningModule ||--o{ QuizAttempt : has
    QuizAttempt ||--o{ QuizAttemptQuestion : contains
```

## Key Tables
- **Users**: Core auth table.
- **SecurityEvents**: Audit log for the SOC dashboard.
- **LabProgress**: User's state in a given lab.
- **QuizAttempt**: Stores session data for testing.
"""

    files["API-DOCUMENTATION.md"] = """# API Documentation

*Based on FastAPI OpenAPI implementation.*

## System (`/api/system`)
- `GET /health` - System health check.
- `GET /dashboard` - Dashboard stats (recent events, threat overview).
- `GET /events` - Security audit logs.
- `GET /progress` - Global user progress.
- `GET /mode` - Fetch global SECURE/VULNERABLE mode.
- `POST /mode` - Toggle mode.
- `GET /report` - Generate summary report.

## Labs (`/api/labs`)
- `GET /` - List all labs.
- `GET /{lab_id}` - Get lab details.
- `GET /{lab_id}/hint` - Get lab hint.
- `POST /attack` - Submit payload to lab engine.
- `GET /{lab_id}/history` - Get attempt history.
- `GET /{lab_id}/progress` - Get specific lab progress.
- `POST /{lab_id}/reset` - Reset lab environment.

## Learning (`/api/learning`)
- `GET /` - List all modules.
- `GET /{module_id}` - Get module and its lessons.
- `GET /{module_id}/lessons/{lesson_id}` - Get lesson content.
- `POST /{module_id}/lessons/{lesson_id}/complete` - Mark complete.
- `POST /{module_id}/quiz/start` - Initiate quiz.
- `POST /quiz/submit` - Grade quiz attempt.
- `GET /quiz/{attempt_id}` - Get ongoing attempt state.

## Authentication (`/api/auth`)
- `POST /login` - Issue JWT token.
- `GET /me` - Get current user profile.
"""

    files["AUTHENTICATION-AUTHORIZATION.md"] = """# Authentication & Authorization

## Implementation
- **JWT (JSON Web Tokens)**: Used for stateless session management.
- **Hashing**: Passwords hashed using standard cryptographic libraries (e.g., passlib).
- **FastAPI Depends**: Endpoints use `Depends(get_current_user)` to enforce authentication.

## Auth Flow
```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI Auth
    participant DB as Database
    
    U->>API: POST /api/auth/login (username, password)
    API->>DB: Query User
    DB-->>API: User Hash
    API->>API: Validate Password
    API-->>U: Return access_token (JWT)
    
    U->>API: GET /api/labs/ (Bearer Token)
    API->>API: Decode & Validate JWT
    API->>DB: Query User ID
    API-->>U: Protected Data
```
"""

    files["SECURITY-DESIGN.md"] = """# Security Design

## Implemented Controls
1. **Authentication**: JWT token validation on all restricted endpoints.
2. **Environment Isolation**: The mock LLM executes purely deterministic pattern matching, meaning arbitrary code execution via payload is fundamentally blocked at the architectural level.
3. **Synthetic Data**: All PII and sensitive data generated in labs is synthetic and hardcoded/generated dynamically.
4. **CORS**: Configured securely via FastAPI middleware.
5. **Audit Logging**: Every attack attempt, successful or failed, is logged to `SecurityEvent`.

## Planned / Future Enhancements
- Rate Limiting (Redis-based)
- Strict RBAC (Admin vs. Student roles)
- Advanced WAF integration
"""

    files["EVIDENCE-AND-REPORTING.md"] = """# Evidence & Reporting

## Pipeline
The platform simulates real-world Penetration Testing workflows.

```mermaid
flowchart TD
    A[Lab Attack Submitted] --> B[Mock LLM Evaluation]
    B --> C{Is Vulnerable?}
    C -->|Yes| D[Extract Flag / Evidence String]
    D --> E[Save LabAttempt]
    E --> F[Log SecurityEvent(High Severity)]
    F --> G[Generate Live Report PDF/JSON]
```

## Report Generation
Reports are generated dynamically on request (`GET /api/system/report`) by aggregating all `SecurityEvents` marked as `Vulnerable` by the current user.
"""

    files["MONITORING-AND-EVENTS.md"] = """# Monitoring & Events (SIEM)

## Overview
The application features a built-in SOC/SIEM interface.

## Event Structure
- **Timestamp**: Time of execution.
- **Username**: Initiating identity.
- **Attack Type**: Classification (e.g., PROMPT_INJECTION, RAG_POISONING).
- **Severity**: HIGH, MEDIUM, LOW.
- **Result**: Vulnerable or Blocked.
- **Endpoint**: Lab identifier.

## Flow
```mermaid
flowchart LR
    A[Lab Engine] -->|fires event| B(Event Dispatcher)
    B --> C[(SQLite: SecurityEvent)]
    C --> D[SOC Dashboard View]
```
"""

    files["TESTING.md"] = """# Testing

## Implemented Tests
The project utilizes `pytest` for backend testing.

- **`test_api.py`**: Integration tests for general API endpoints, auth, and dashboard metrics.
- **`test_learning.py`**: Tests the quiz generation, completion, and scoring logic.

## How to Run Tests
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run tests
pytest -q tests/test_learning.py tests/test_api.py
```
"""

    files["DEPLOYMENT.md"] = """# Deployment (Local)

## Prerequisites
- Python 3.10+
- `pip`

## Instructions
1. **Virtual Environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
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
   ```
"""

    files["VERCEL-DEPLOYMENT.md"] = """# Vercel Deployment

*STATUS: PLANNED DEPLOYMENT*

## Architecture Concept
```mermaid
graph TD
    GH[GitHub Repo] --> V[Vercel Serverless]
    V --> F[Static Frontend Build]
    V --> B[FastAPI Serverless Functions]
    B --> DB[(PostgreSQL / Supabase)]
```

## Considerations for Production
1. **Storage**: SQLite is **not supported** natively on Vercel due to the ephemeral serverless environment. A managed PostgreSQL database (e.g., Supabase, Neon) must be configured via environment variables.
2. **Build Step**: Configure `vercel.json` to route `/api/*` to FastAPI, and serve `frontend/` as static assets.
3. **Secrets**: Update Vercel environment variables with secure `JWT_SECRET_KEY` and `DATABASE_URL`.
"""

    files["15-LABS.md"] = """# 15 AI Security Labs

*Documenting the 15 labs currently implemented in the database.*

## Lab 01 — Direct Prompt Injection
**Objective**: Force the LLM to ignore instructions and print a secret.
**Vulnerable Behavior**: The LLM blindly concatenates user input with system prompts.
**Secure Behavior**: The LLM sanitizes input or strictly separates user context from system context.

## Lab 02 — System Prompt Extraction
**Objective**: Extract the hidden system prompt guidelines.
**Vulnerable Behavior**: The LLM regurgitates its initial programming when requested.

## Lab 03 — Jailbreak Testing
**Objective**: Bypass safety filters to generate disallowed content.
**Vulnerable Behavior**: The LLM fails to recognize adversarial framing (e.g., "DAN" mode).

## Lab 04 — Sensitive Information Disclosure
**Objective**: Trick the LLM into revealing PII or API keys embedded in its context.
**Vulnerable Behavior**: The LLM lacks output filtering for sensitive tokens.

## Lab 05 — RAG Security
**Objective**: Access documents outside the intended scope of the user.
**Vulnerable Behavior**: The retriever uses unsanitized input to fetch cross-tenant data.

## Lab 06 — RAG Poisoning
**Objective**: Inject a document into the knowledge base that manipulates future answers.
**Vulnerable Behavior**: The system ingests untrusted text without validation.

## Lab 07 — Indirect Prompt Injection
**Objective**: Embed an injection payload on a webpage that the LLM reads.
**Vulnerable Behavior**: The LLM executes instructions found in retrieved web text.

## Lab 08 — Insecure Output Handling
**Objective**: Achieve XSS by making the LLM generate unescaped HTML/JS.
**Vulnerable Behavior**: The frontend renders LLM output as raw HTML.

## Lab 09 — Excessive Agency
**Objective**: Make an AI agent execute a destructive action (e.g., drop database).
**Vulnerable Behavior**: The agent has overly broad permissions without human-in-the-loop.

## Lab 10 — AI Agent Tool Abuse
**Objective**: Exploit a vulnerability in a tool the AI uses (e.g., SSRF via a fetch tool).
**Vulnerable Behavior**: The agent blindly passes user-controlled parameters to backend APIs.

## Lab 11 — Broken Access Control
**Objective**: Exploit flawed RBAC in the LLM's authorization layer.
**Vulnerable Behavior**: The LLM serves responses based on user claims rather than backend validation.

## Lab 12 — Cross-Tenant AI Data Access
**Objective**: View data belonging to another tenant in a multi-tenant LLM deployment.
**Vulnerable Behavior**: Vector search lacks tenant isolation.

## Lab 13 — AI Supply Chain Security
**Objective**: Identify a vulnerability in an imported third-party AI library/model.
**Vulnerable Behavior**: The application uses a known-vulnerable dependency.

## Lab 14 — Model/Prompt Configuration Security
**Objective**: Abuse insecure generation parameters (e.g., high temperature leading to leakage).
**Vulnerable Behavior**: The model configuration is optimized for creativity over security.

## Lab 15 — AI Security Assessment
**Objective**: Comprehensive capstone combining multiple vulnerabilities.
**Vulnerable Behavior**: The system exhibits chained vulnerabilities.
"""

    files["CONTRIBUTING.md"] = """# Contributing

## Adding a New Lab
1. Define the lab metadata in `app/models/core.py` (or seed script).
2. Create a new `Target` class in `app/services/targets.py`.
3. Implement `_evaluate_vulnerable` and `_evaluate_secure` methods using regex/string matching.
4. Update `LabEngine` to route to the new target.

## Adding a Learning Module
1. Define the module and lessons in `scripts/seed_learning.py`.
2. Add corresponding quiz questions to the seed script.
3. Run `python scripts/seed_learning.py` to populate the SQLite database.

## PR Process
1. Run `pytest` locally.
2. Ensure no UI breakages in the SPA.
3. Submit PR with detailed description.
"""

    # Write all files
    for filename, content in files.items():
        filepath = os.path.join(docs_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip() + "\\n")
            
    # Generate diagrams
    diagram_files = {
        "system-architecture.mmd": """graph TD
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
    
    Services --> DB""",
        
        "system-flow.mmd": """flowchart TD
    A[User] --> B[Login]
    B --> C{Dashboard}
    
    C -->|Selects Lab| D[Lab Detail]
    D --> E[Read Objective]
    E --> F[Send Attack Payload]
    F --> G[Lab Engine]
    G --> H[Mock Target Evaluation]
    H --> I{Vulnerability Detected?}
    I -->|Yes| J[Capture Evidence]
    I -->|No| K[Return Standard Response]
    J --> L[Update Progress]
    J --> M[Log Security Event]
    L --> N[Generate Final Report]""",

        "request-flow.mmd": """sequenceDiagram
    participant B as Browser
    participant A as API (FastAPI)
    participant LE as Lab Engine
    participant T as Target/MockLLM
    participant DB as Database
    
    B->>A: POST /api/labs/attack (Payload)
    A->>LE: process_interaction(payload)
    LE->>T: evaluate(payload)
    T-->>LE: is_vuln, response, evidence
    LE->>DB: create(LabAttempt)
    LE->>DB: create(SecurityEvent)
    DB-->>LE: OK
    LE-->>A: Evaluation Result
    A-->>B: JSON Response""",

        "authentication-flow.mmd": """sequenceDiagram
    participant U as User
    participant API as FastAPI Auth
    participant DB as Database
    
    U->>API: POST /api/auth/login (username, password)
    API->>DB: Query User
    DB-->>API: User Hash
    API->>API: Validate Password
    API-->>U: Return access_token (JWT)
    
    U->>API: GET /api/labs/ (Bearer Token)
    API->>API: Decode & Validate JWT
    API->>DB: Query User ID
    API-->>U: Protected Data""",

        "lab-execution-flow.mmd": """flowchart TD
    A[User Input Payload] --> B[Lab Engine]
    B --> C{Check System Mode}
    C -->|Secure| D[Target - Apply Mitigations]
    C -->|Vulnerable| E[Target - Unfiltered Evaluation]
    
    D --> F[Blocked/Ineffective]
    E --> G{Contains Attack Pattern?}
    G -->|Yes| H[Vulnerable Output & Evidence]
    G -->|No| I[Standard Safe Output]""",

        "learning-flow.mmd": """flowchart TD
    A[Start Module] --> B[Read Lessons]
    B --> C[Mark Lessons Complete]
    C --> D[Take Module Quiz]
    D --> E{Pass >= 70%?}
    E -->|Yes| F[Module Completed]
    E -->|No| G[Retry Quiz]
    F --> H[Unlock Related Labs]""",

        "quiz-flow.mmd": """sequenceDiagram
    participant User
    participant Front as Frontend
    participant API
    participant DB
    
    User->>Front: Start Quiz
    Front->>API: POST /api/learning/{mod}/quiz/start
    API->>DB: Create QuizAttempt
    API-->>Front: Return Question IDs & Text
    User->>Front: Submits Answers
    Front->>API: POST /api/learning/quiz/submit
    API->>DB: Evaluate & Update QuizAttempt
    API-->>Front: Score & Explanations""",

        "progress-flow.mmd": """flowchart TD
    A[User Action] --> B{Action Type}
    B -->|Submit Quiz| C[Update ModuleProgress]
    B -->|Exploit Vulnerability| D[Update LabProgress]
    C --> E[Global Progress Engine]
    D --> E
    E --> F[Dashboard Statistics Updated]""",

        "evidence-flow.mmd": """flowchart TD
    A[Lab Attack Submitted] --> B[Mock LLM Evaluation]
    B --> C{Is Vulnerable?}
    C -->|Yes| D[Extract Flag / Evidence String]
    D --> E[Save LabAttempt]
    E --> F[Log SecurityEvent]
    F --> G[Generate Live Report]""",

        "report-flow.mmd": """flowchart TD
    A[Request Report] --> B[Fetch SecurityEvents]
    B --> C{Filter Vulnerable}
    C --> D[Aggregate Findings]
    D --> E[Format Summary]
    E --> F[Return Report Data]""",

        "prompt-injection-flow.mmd": """flowchart TD
    A[User Input] --> B[System Prompt Wrapper]
    B --> C[LLM Evaluation]
    C --> D{Instruction Override Detected?}
    D -->|Yes| E[Unexpected Action Executed]
    D -->|No| F[Normal Response]""",
    
        "rag-flow.mmd": """flowchart TD
    A[User Query] --> B[Retriever]
    B --> C[(Knowledge Base)]
    C --> D[Retrieved Context]
    D --> E[LLM Generation]
    E --> F[Response]""",

        "rag-poisoning-flow.mmd": """flowchart TD
    A[Malicious Document] --> B[(Knowledge Base)]
    C[User Query] --> D[Retriever]
    D --> B
    D --> E[Retrieve Poisoned Context]
    E --> F[LLM Generation]
    F --> G[Manipulated Output Provided to User]""",
    
        "indirect-prompt-injection-flow.mmd": """flowchart TD
    A[External Content] --> B[Retriever / Web Tool]
    B --> C[Injected Instruction]
    C --> D[LLM Generation]
    D --> E[Unexpected Behavior]""",

        "ai-agent-flow.mmd": """flowchart TD
    A[User Prompt] --> B[AI Agent]
    B --> C{Tool Selection}
    C --> D[API Tool]
    C --> E[DB Tool]
    D --> F[Execution]
    E --> F
    F --> G[Response Generation]""",

        "excessive-agency-flow.mmd": """flowchart TD
    A[User Prompt] --> B[AI Agent]
    B --> C{Permission Check?}
    C -->|Missing / Flawed| D[Execute Highly Privileged Tool]
    C -->|Proper| E[Access Denied]
    D --> F[Data Exfiltration / Modification]""",

        "access-control-flow.mmd": """flowchart TD
    A[User Request] --> B[API Layer]
    B --> C{RBAC Check}
    C -->|Authorized| D[Proceed]
    C -->|Unauthorized| E[403 Forbidden]""",

        "security-event-flow.mmd": """flowchart LR
    A[Lab Engine] -->|fires event| B(Event Dispatcher)
    B --> C[(SQLite: SecurityEvent)]
    C --> D[SOC Dashboard View]""",

        "deployment-flow.mmd": """graph TD
    GH[GitHub Repo] --> V[Vercel Serverless]
    V --> F[Static Frontend Build]
    V --> B[FastAPI Serverless Functions]
    B --> DB[(PostgreSQL / Supabase)]"""
    }

    for filename, content in diagram_files.items():
        filepath = os.path.join(diagrams_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip() + "\\n")
            
    print("Documentation generation complete.")

if __name__ == '__main__':
    create_docs()
