from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Any, Union, Optional
from pydantic import field_validator

class Settings(BaseSettings):
    """Application settings."""
    
    # Lean4Web API
    lean4web_url: str = "https://live.lean-lang.org"
    
    # CORS
    # Allow string (for comma-separated env vars) or list
    cors_origins: Union[str, list[str]] = ["http://localhost:5173", "http://127.0.0.1:5173", "*"]
    
    @field_validator("cors_origins", mode="after")
    @classmethod
    def parse_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            # If it looks like JSON list, try to parse it
            if v.strip().startswith("["):
                import json
                try:
                    return json.loads(v)
                except:
                    pass
            # Otherwise treat as comma-separated string
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v
    
    # App
    debug: bool = True
    
    # AI Integration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    
    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
