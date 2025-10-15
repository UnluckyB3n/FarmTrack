from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Farm Traceability System"
    DATABASE_URL: str
    SECRET_KEY: str
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
