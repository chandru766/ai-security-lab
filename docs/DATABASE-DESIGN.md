# Database Design

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
- **QuizAttempt**: Stores session data for testing.\n