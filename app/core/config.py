from __future__ import annotations

import redis

from redis.client import Redis

from enum import Enum
from pydantic import PostgresDsn, field_validator, BaseModel
from pydantic_settings import BaseSettings
from pydantic_core.core_schema import FieldValidationInfo
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    page: str = "/page"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()


class Settings(BaseSettings):
    class Environment(str, Enum):
        local = "local"
        dev = "dev"
        prod = "prod"

    PROJECT_NAME: str = "Cehcom API"

    # Environment settings
    ENVIRONMENT: Environment = Environment.dev  # local, dev, prod
    COUNTRY_ISO: str = "RU"

    # Telegram
    TG_TOKEN: str = ""

    # Redis
    REDIS_HOST: str = "redis"
    
    # Mongo
    MONGO_USER: str
    MONGO_PASSWORD: str
    MONGO_SERVER: str
    MONGO_DB: str
    MONGO_PORT: int
    MONGO_URL: str = None
    
    # Ollama Url
    OLLAMA_URL: str = "http://localhost:11435"

    # # Database settings
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int
    POSTGRES_ECHO: bool = False
    SQLALCHEMY_DATABASE_URL: PostgresDsn | None = None

    # JWT Settings
    JWT_SECRET_KEY: str = "jwt_secret_key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 100
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    api: ApiPrefix = ApiPrefix()

    @field_validator("SQLALCHEMY_DATABASE_URL", mode="after")
    def assemble_db_connection(cls, v: str, values: FieldValidationInfo) -> str:
        if v is not None:
            if isinstance(v, str):
                return v
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                port=values.data.get("POSTGRES_PORT"),
                username=values.data.get("POSTGRES_USER"),
                password=values.data.get("POSTGRES_PASSWORD"),
                host=values.data.get("POSTGRES_SERVER"),
                path=f"{values.data.get('POSTGRES_DB') or ''}",
            )
        )
        
    @field_validator("MONGO_URL", mode="after")
    def assemble_mongo_connection(cls, v: str, values: FieldValidationInfo) -> str:
        if values.data.get("MONGO_URL") is not None:
            return values.data.get("MONGO_URL")
        return f"mongodb://{values.data.get('MONGO_USER')}:{values.data.get('MONGO_PASSWORD')}@{values.data.get('MONGO_SERVER')}:{values.data.get('MONGO_PORT')}/{values.data.get('MONGO_DB')}"


settings = Settings()

red: Redis = redis.Redis(host=settings.REDIS_HOST, port=6379, db=0)
