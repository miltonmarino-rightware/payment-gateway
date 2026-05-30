from functools import lru_cache
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    app_env: Literal["development", "test", "staging", "production"] = Field(default="development", alias="APP_ENV")
    app_version: str = Field(default="0.2.0", alias="APP_VERSION")
    app_name: str = Field(default="RightWare Payment Gateway", alias="APP_NAME")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    database_url: str = Field(alias="DATABASE_URL")
    redis_url: str = Field(alias="REDIS_URL")
    api_key_pepper: str = Field(alias="API_KEY_PEPPER")
    hmac_secret: str = Field(alias="HMAC_SECRET")
    aes_secret_key: str = Field(alias="AES_SECRET_KEY")
    stripe_secret_key: str | None = Field(default=None, alias="STRIPE_SECRET_KEY")
    stripe_webhook_secret: str | None = Field(default=None, alias="STRIPE_WEBHOOK_SECRET")
    rate_limit_requests: int = Field(default=10, alias="RATE_LIMIT_REQUESTS")
    rate_limit_window_seconds: int = Field(default=60, alias="RATE_LIMIT_WINDOW_SECONDS")
    allow_sandbox_raw_card_input: bool = Field(default=False, alias="ALLOW_SANDBOX_RAW_CARD_INPUT")
    @property
    def is_production(self) -> bool: return self.app_env == "production"
    @property
    def stripe_configured(self) -> bool: return bool(self.stripe_secret_key)

@lru_cache
def get_settings() -> Settings:
    return Settings()
