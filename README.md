# 🔐 AI Security Lab

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
![System Architecture](docs/diagrams/system-architecture.mmd)

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

## Documentation
Please refer to the comprehensive [Documentation Index](docs/README.md) for full details on architecture, flows, APIs, labs, and deployment.

## Installation & Deployment
For detailed instructions on running locally or deploying to Vercel, see [Deployment Docs](docs/DEPLOYMENT.md).

## Testing
Run the backend test suite:
```bash
python -m pytest -q tests/test_learning.py tests/test_api.py
```

## Security Notice
⚠ **EDUCATIONAL ENVIRONMENT**
All labs are designed for authorized, local security training and use synthetic data. Do not execute these attacks against systems you do not have permission to test.

## Author
Created & Developed by:
**Chandrasekar L**
Cybersecurity | AI Security | AI Red Teaming
