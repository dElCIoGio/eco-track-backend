from functools import lru_cache


from app.core.config import settings, Settings
from app.db import MongoDB


def get_settings():
    return Settings()


@lru_cache()
def get_db():
    return MongoDB().get_db()


