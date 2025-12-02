from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Farm Traceability System"
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = True
    
    # Google OAuth Settings
    GOOGLE_CLIENT_ID: Optional[str] = None
    GOOGLE_CLIENT_SECRET: Optional[str] = None

    class Config:
        env_file = ".env"

settings = Settings()
