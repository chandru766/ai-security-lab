# Learning Engine

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
```\n