from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Backup Manager"
    PROJECT_VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DATABASE_URL: str = "sqlite:///./backup_manager.db"
    
    # SMTP Configuration
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 25
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM_EMAIL: str = "admin@wiltel.com.ar"
    SMTP_RECIPIENTS: str = "noc@wiltel.com.ar" # Comma separated list

    class Config:
        env_file = ".env"

settings = Settings()
