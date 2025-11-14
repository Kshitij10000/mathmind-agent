# core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    
    GEMINI_API_KEY: str
    QDRANT_COLLECTION_NAME: str
    QDRANT_API_KEY: str
    QDRANT_URL: str
    VECTOR_DIMENSIONS: int = 768
    TAVILY_API: str
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True, extra="ignore")

settings = Settings()