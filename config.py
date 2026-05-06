import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    app_name: str = os.getenv("APP_NAME", "AI Content Generator")
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"

    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    stability_api_key: str = os.getenv("STABILITY_API_KEY", "")

    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./content.db")
    storage_path: str = os.getenv("STORAGE_PATH", "./storage")

settings = Settings()