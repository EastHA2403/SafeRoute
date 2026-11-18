from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]  # backend/


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    LOG_LEVEL: str = "INFO"
    NODES_CSV: Path = BASE_DIR / "data/processed/nodes.csv"
    EDGES_CSV: Path = BASE_DIR / "data/processed/edges.csv"
    ACCIDENTS_CSV: Path = BASE_DIR / "data/processed/accidents.csv"
    CORS_ORIGINS: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500"]


settings = Settings()

