# Evidence & Reporting

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
Reports are generated dynamically on request (`GET /api/system/report`) by aggregating all `SecurityEvents` marked as `Vulnerable` by the current user.\n