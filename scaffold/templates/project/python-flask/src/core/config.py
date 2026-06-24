import os


class Config:
    # Obrigatório — sem default intencional para forçar configuração explícita
    SECRET_KEY: str = os.environ["SECRET_KEY"]
    TESTING: bool = False
    WTF_CSRF_ENABLED: bool = True
    ENV: str = os.environ.get("FLASK_ENV", "development")


class DevelopmentConfig(Config):
    DEBUG: bool = True
    # Desabilitar CSRF em dev local se for API-only
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(Config):
    DEBUG: bool = False
    SESSION_COOKIE_SECURE: bool = True
    SESSION_COOKIE_HTTPONLY: bool = True
    SESSION_COOKIE_SAMESITE: str = "Lax"
    ENV: str = "production"


class TestingConfig(Config):
    TESTING: bool = True
    WTF_CSRF_ENABLED: bool = False
    SECRET_KEY: str = "test-secret-key-nao-usar-em-producao"  # noqa: S105


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
