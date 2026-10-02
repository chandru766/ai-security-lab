# Authentication & Authorization

## Implementation
- **JWT (JSON Web Tokens)**: Used for stateless session management.
- **Hashing**: Passwords hashed using standard cryptographic libraries (e.g., passlib).
- **FastAPI Depends**: Endpoints use `Depends(get_current_user)` to enforce authentication.

## Auth Flow
```mermaid
sequenceDiagram
    participant U as User
    participant API as FastAPI Auth
    participant DB as Database
    
    U->>API: POST /api/auth/login (username, password)
    API->>DB: Query User
    DB-->>API: User Hash
    API->>API: Validate Password
    API-->>U: Return access_token (JWT)
    
    U->>API: GET /api/labs/ (Bearer Token)
    API->>API: Decode & Validate JWT
    API->>DB: Query User ID
    API-->>U: Protected Data
```\n