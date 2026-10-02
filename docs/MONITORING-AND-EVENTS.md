# Monitoring & Events (SIEM)

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
```\n