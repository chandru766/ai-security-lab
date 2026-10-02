# AI Security Flows

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
```\n