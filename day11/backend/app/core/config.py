from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    APP_NAME: str = "ATS Resume Optimizer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    SECRET_KEY: str = "change-me-in-production-use-32-char-min"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./ats_optimizer.db"

    # Ollama
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_RESUME_PARSE_MODEL: str = "qwen3:8b"
    OLLAMA_ATS_MODEL: str = "qwen3:8b"
    OLLAMA_OPTIMIZE_MODEL: str = "qwen3:latest"
    OLLAMA_COVER_LETTER_MODEL: str = "qwen3:latest"
    OLLAMA_COLD_EMAIL_MODEL: str = "qwen3:latest"
    OLLAMA_FAST_MODEL: str = "llama3.2:3b"
    OLLAMA_EMBED_MODEL: str = "nomic-embed-text"

    # OpenRouter (free models)
    OPENROUTER_API_KEY: str = ""
    OPENROUTER_BASE_URL: str = "https://openrouter.ai/api/v1"
    OPENROUTER_RESUME_PARSE_MODEL: str = "google/gemma-4-31b-it:free"
    OPENROUTER_ATS_MODEL: str = "google/gemma-4-31b-it:free"
    OPENROUTER_OPTIMIZE_MODEL: str = "google/gemma-4-31b-it:free"
    OPENROUTER_COVER_LETTER_MODEL: str = "google/gemma-4-31b-it:free"
    OPENROUTER_COLD_EMAIL_MODEL: str = "google/gemma-4-31b-it:free"
    OPENROUTER_FAST_MODEL: str = "google/gemma-4-31b-it:free"
    USE_OPENROUTER: bool = True

    # ChromaDB
    CHROMA_PATH: str = "./chroma_db"
    CHROMA_COLLECTION: str = "resumes"

    # File Storage
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE_MB: int = 10

    # CORS
    ALLOWED_ORIGINS: str = '["http://localhost:3000","http://127.0.0.1:3000"]'

    # JWT
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    def get_allowed_origins(self) -> List[str]:
        try:
            return json.loads(self.ALLOWED_ORIGINS)
        except Exception:
            return ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
