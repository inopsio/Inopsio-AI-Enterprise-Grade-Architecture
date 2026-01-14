"""
Inopsio AI Enterprise - Application Settings
Uses pydantic-settings for type-safe environment variable management.
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Inopsio AI Enterprise API"
    
    # Security
    SECRET_KEY: str = "super_secret_key_here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = "postgresql://inopsio_admin:password@localhost:5432/inopsio_db"
    
    # CORS - Origins allowed to call this API
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # External Services (Optional)
    GEMINI_API_KEY: str = ""
    STRIPE_SECRET_KEY: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
