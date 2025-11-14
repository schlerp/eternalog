import os
from pydantic import BaseModel


class Settings(BaseModel):
    sqlalchemy_database_url: str = os.getenv(
        "ETERNALOG_SQLALCHEMY_DATABASE_URL", "sqlite:///./eternalog.db"
    )
    environment: str = os.getenv("ETERNALOG_ENVIRONMENT", "development")


def get_settings() -> Settings:
    return Settings()
