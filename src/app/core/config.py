from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    TITLE: str = 'Organizations Directory'
    DEBUG: bool = Field(default=False, alias='DEBUG')

    DOCS_URL: str = '/api/docs'
    OPENAPI_URL: str = '/api/docs.json'
    REDOC_URL: str = '/api/redoc'

    DB_HOST: str = Field(..., alias='DB_HOST')
    DB_PORT: str = Field(..., alias='DB_PORT')
    DB_NAME: str = Field(..., alias='DB_NAME')
    DB_USER: str = Field(..., alias='DB_USER')
    DB_PASS: str = Field(..., alias='DB_PASS')

    @property
    def DB_URI(self) -> str:
        return f'postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'

    @property
    def SYNC_DB_URI(self) -> str:
        return f'postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


@lru_cache
def get_config() -> Config:
    return Config()


config = get_config()
