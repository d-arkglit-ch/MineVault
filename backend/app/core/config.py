import os
from pathlib import Path
from typing import List

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
ROOT_DIR = BACKEND_DIR.parent

# Pre-load environment variables from backend/.env or root .env into os.environ
try:
    from dotenv import load_dotenv
    if (BACKEND_DIR / ".env").exists():
        load_dotenv(dotenv_path=BACKEND_DIR / ".env", override=False)
    if (ROOT_DIR / ".env").exists():
        load_dotenv(dotenv_path=ROOT_DIR / ".env", override=False)
except ImportError:
    pass

try:
    from pydantic_settings import BaseSettings, SettingsConfigDict

    class Settings(BaseSettings):
        PROJECT_NAME: str = "GeoMine AI Backend (SIH26023)"
        API_V1_STR: str = "/api/v1"
        DEBUG: bool = True
        
        # CORS
        FRONTEND_ORIGIN: str = "http://localhost:3000"
        BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

        # Database & Storage
        DATABASE_URL: str = f"sqlite:///{(BACKEND_DIR / 'geomine.db').resolve().as_posix()}"
        CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
        STORAGE_DIR: str = "./uploads"

        # AI & Multi-Agent Keys
        GEMINI_API_KEY: str = ""
        GOOGLE_VISION_API_KEY: str = ""
        OPENAI_API_KEY: str = ""

        model_config = SettingsConfigDict(
            env_file=(str(BACKEND_DIR / ".env"), str(ROOT_DIR / ".env"), ".env"),
            env_file_encoding="utf-8",
            extra="ignore",
            case_sensitive=True,
        )

except ImportError:
    from pydantic import BaseModel
    class BaseSettings(BaseModel):
        def __init__(self, **values):
            super().__init__(**values)
            # Read env vars if available
            for field in self.model_fields:
                if field in os.environ:
                    val = os.environ[field]
                    current_val = getattr(self, field)
                    if isinstance(current_val, list):
                        setattr(self, field, [v.strip() for v in val.split(",") if v.strip()])
                    elif isinstance(current_val, bool):
                        setattr(self, field, val.lower() in ("true", "1", "yes"))
                    else:
                        setattr(self, field, val)

    class Settings(BaseSettings):
        PROJECT_NAME: str = "GeoMine AI Backend (SIH26023)"
        API_V1_STR: str = "/api/v1"
        DEBUG: bool = True
        
        # CORS
        FRONTEND_ORIGIN: str = "http://localhost:3000"
        BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

        # Database & Storage
        DATABASE_URL: str = "sqlite+aiosqlite:///./geomine.db"
        CHROMA_PERSIST_DIRECTORY: str = "./chroma_db"
        STORAGE_DIR: str = "./uploads"

        # AI & Multi-Agent Keys
        GEMINI_API_KEY: str = ""
        GOOGLE_VISION_API_KEY: str = ""
        OPENAI_API_KEY: str = ""

settings = Settings()

