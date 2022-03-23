import os
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    db_url: str = Field(..., env='DATABASE_URL')

try:
    settings = Settings()
except:
    os.environ['DATABASE_URL'] = 'postgresql://fastapi_satellogic:fastapi_satellogic@localhost:5433/fastapi_satellogic'
    settings = Settings()