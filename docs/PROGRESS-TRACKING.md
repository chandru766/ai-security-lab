# Progress Tracking

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
```\n