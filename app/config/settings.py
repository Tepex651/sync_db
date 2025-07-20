from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="POSTGRES_", extra="ignore"
    )

    host: str
    port: int
    db: str
    user: str
    password: SecretStr

    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db}"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database: PostgresSettings = Field(default_factory=PostgresSettings)
    data_refresh_interval_seconds: int


settings = Settings()
