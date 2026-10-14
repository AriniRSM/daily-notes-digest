from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    database_url: str = "postgresql+psycopg://arinirsm@localhost:5432/daily_notes_digest"

    groq_api_key: str | None = None
    groq_model_id: str = Field(
        default="qwen/qwen3.8-27b",
        validation_alias="GROQ_MODEL_ID",
    )

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        extra="ignore",
    )


settings = Settings()
