# System Flow

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
```\n