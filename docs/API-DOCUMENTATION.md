# API Documentation

*Based on FastAPI OpenAPI implementation.*

## System (`/api/system`)
- `GET /health` - System health check.
- `GET /dashboard` - Dashboard stats (recent events, threat overview).
- `GET /events` - Security audit logs.
- `GET /progress` - Global user progress.
- `GET /mode` - Fetch global SECURE/VULNERABLE mode.
- `POST /mode` - Toggle mode.
- `GET /report` - Generate summary report.

## Labs (`/api/labs`)
- `GET /` - List all labs.
- `GET /{lab_id}` - Get lab details.
- `GET /{lab_id}/hint` - Get lab hint.
- `POST /attack` - Submit payload to lab engine.
- `GET /{lab_id}/history` - Get attempt history.
- `GET /{lab_id}/progress` - Get specific lab progress.
- `POST /{lab_id}/reset` - Reset lab environment.

## Learning (`/api/learning`)
- `GET /` - List all modules.
- `GET /{module_id}` - Get module and its lessons.
- `GET /{module_id}/lessons/{lesson_id}` - Get lesson content.
- `POST /{module_id}/lessons/{lesson_id}/complete` - Mark complete.
- `POST /{module_id}/quiz/start` - Initiate quiz.
- `POST /quiz/submit` - Grade quiz attempt.
- `GET /quiz/{attempt_id}` - Get ongoing attempt state.

## Authentication (`/api/auth`)
- `POST /login` - Issue JWT token.
- `GET /me` - Get current user profile.\n