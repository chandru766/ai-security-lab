# Quiz System

## Overview
The quiz system provides a server-side validated assessment environment to test user comprehension.

## Features
- **Server-Side Validation**: Answers are not exposed in the frontend.
- **Attempt Tracking**: `QuizAttempt` and `QuizAttemptQuestion` models track user history.
- **Explanation Feedback**: The backend returns explanations for correct/incorrect answers upon submission.

## Flow
```mermaid
sequenceDiagram
    participant User
    participant Front as Frontend
    participant API
    participant DB
    
    User->>Front: Start Quiz
    Front->>API: POST /api/learning/{mod}/quiz/start
    API->>DB: Create QuizAttempt
    API-->>Front: Return Question IDs & Text
    User->>Front: Submits Answers
    Front->>API: POST /api/learning/quiz/submit
    API->>DB: Evaluate & Update QuizAttempt
    API-->>Front: Score & Explanations
```\n