# Security Design

## Implemented Controls
1. **Authentication**: JWT token validation on all restricted endpoints.
2. **Environment Isolation**: The mock LLM executes purely deterministic pattern matching, meaning arbitrary code execution via payload is fundamentally blocked at the architectural level.
3. **Synthetic Data**: All PII and sensitive data generated in labs is synthetic and hardcoded/generated dynamically.
4. **CORS**: Configured securely via FastAPI middleware.
5. **Audit Logging**: Every attack attempt, successful or failed, is logged to `SecurityEvent`.

## Planned / Future Enhancements
- Rate Limiting (Redis-based)
- Strict RBAC (Admin vs. Student roles)
- Advanced WAF integration\n