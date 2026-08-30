import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Smart Medical Diagnosis Assistant"
    API_V1_STR: str = "/api/v1"
    VERSION: str = "0.1.0"

    # Security
    SECRET_KEY: str = "smda-secret-key-change-in-production-super-secure-jwt-secret-key-32chars"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # Databases
    DATABASE_URL: str = "sqlite:///./smda.db"
    REDIS_URL: str = "redis://localhost:6379/0"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080",
        "http://localhost:5000",
        "http://127.0.0.1:8000",
        "*"
    ]

    # Clinical Disclaimers
    MEDICAL_DISCLAIMER: str = (
        "SMDA is an educational and clinical decision-support tool. It is NOT a substitute "
        "for professional medical diagnosis, advice, or treatment. Always seek the advice "
        "of your physician or other qualified healthcare provider."
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


settings = Settings()
