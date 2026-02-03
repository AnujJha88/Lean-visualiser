from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Any
from pydantic import field_validator

class Settings(BaseSettings):
    """Application settings."""
    
    # Lean4Web API
    lean4web_url: str = "https://live.lean-lang.org"
    
    # CORS
    cors_origins: list[str] = ["http://localhost:5173", "http://127.0.0.1:5173", "*"]
    
    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> Any:
        if isinstance(v, str) and not v.startswith("["):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    # App
    debug: bool = True
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
