# Lab Engine

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
```\n