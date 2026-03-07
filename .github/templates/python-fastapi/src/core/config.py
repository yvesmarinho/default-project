from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "my-api"
    VERSION: str = "0.1.0"
    ENV: str = "development"
    # SECRET_KEY é obrigatório — não tem default intencional
    SECRET_KEY: str
    DATABASE_URL: str | None = None
    ALLOWED_ORIGINS: list[str] = ["http://localhost:3000"]


settings = Settings()
