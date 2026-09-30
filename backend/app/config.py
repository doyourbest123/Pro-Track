import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE_PATH = BASE_DIR.parent / "key.env"

class Settings(BaseSettings):
    PROJECT_NAME: str = "ProTrack Backend"
    DEBUG: bool = True

    DATA_DIR: Path = BASE_DIR / "data"
    PORTFOLIO_FILE_PATH: Path = DATA_DIR / "user_portfolio.json"

    # CORS Middleware Settings
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:8000",
    ]

    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=ENV_FILE_PATH,
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()