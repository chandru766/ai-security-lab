from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Security Lab V2"
    SECRET_KEY: str = "super-secret-key-for-lab-only"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    DATABASE_URL: str = "sqlite:///./data/ai_security_lab.db"
    LLM_PROVIDER: str = "mock"

settings = Settings()
