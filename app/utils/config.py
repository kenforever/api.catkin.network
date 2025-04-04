from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import Enum


class Environment(Enum):
    PRODUCTION = "production"
    DEVELOPMENT = "development"


class Settings(BaseSettings):
    ENV: Environment = Environment.PRODUCTION

    # class Config:
    #     env_file = ".env"
    #     env_file_encoding = "utf-8"

    JWT_SECRET: str
    JWT_EXPIRE_MINUTES: int = 10080

    SUPABASE_SERVICE_KEY: str
    SUPABASE_URL: str
    DATABASE_SCHEMA: str

    # Common
    APP_DOMAIN: str


    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str
    REDIS_SSL: bool = True


config = Settings()

# print(config.model_dump())
