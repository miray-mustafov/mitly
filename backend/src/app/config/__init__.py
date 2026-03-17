import os
from functools import lru_cache

ENV = os.getenv("ENV", "dev")

if ENV == "prod":
    from .prod import Settings
elif ENV == "test":
    from .test import Settings
else:
    from .dev import Settings


@lru_cache
def get_settings() -> Settings:
    """
    lru_cache = Last Recently Used Cache
    Caches the settings initially and then retrieves them from memory instead of reading them every time.
        + Performance:
        + Consistency: It guarantees that the same instance of the settings is used across your entire application.
    """

    return Settings()


settings = get_settings()
