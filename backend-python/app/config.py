from functools import lru_cache
from app.logic.entities import Settings

@lru_cache()
def get_settings() -> Settings:
    """Singleton di configurazione."""
    return Settings()