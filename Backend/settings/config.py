from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from sqlalchemy.engine import URL
from typing import Optional


class DataBaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=[".env", "../.env", "/app/.env"])

    user: str = Field(default="postgres", alias="DB_USER")
    password: str = Field(default="postgres", alias="DB_PASSWORD")
    db_name: str = Field(default="postgres", alias="DB_NAME")
    host: str = Field(default="postgres", alias="DB_HOST")
    port: int = 5432

    def get_connection_string(self) -> str:
        return URL.create(
            drivername="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.db_name,
        ).render_as_string(hide_password=False)


class RedisConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=[".env", "../.env", "/app/.env"])

    host: str = Field(default="redis", alias="REDIS_HOST")
    port: int = Field(default=6379, alias="REDIS_PORT")

    def get_url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"


class JWTConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=[".env", "../.env", "/app/.env"])

    secret_key: str = Field(default="super-secret-key-change-me-in-production", alias="JWT_SECRET_KEY")
    algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    expiry_minutes: int = Field(default=1440, alias="JWT_EXPIRY_MINUTES")


class LLMConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=[".env", "../.env", "/app/.env"])

    provider: Optional[str] = Field(default=None, alias="LLM_PROVIDER")
    api_key: Optional[str] = Field(default=None, alias="LLM_API_KEY")
    model_name: Optional[str] = Field(default=None, alias="LLM_MODEL")


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_file=[".env", "../.env", "/app/.env"])

    seed_username: str = Field(default="admin", alias="SEED_USERNAME")
    seed_password: str = Field(default="admin", alias="SEED_PASSWORD")


class Config:
    def __init__(self):
        self.db = DataBaseConfig()
        self.redis = RedisConfig()
        self.jwt = JWTConfig()
        self.llm = LLMConfig()
        self.app = AppConfig()


config = Config()