from flask import Flask

from src.blueprints.health import health_bp
from src.core.config import config
from src.extensions import csrf, talisman


def create_app(config_name: str = "development") -> Flask:
    """Application factory."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Extensões
    csrf.init_app(app)
    talisman.init_app(
        app,
        force_https=app.config.get("ENV") == "production",
        content_security_policy=False,
    )

    # Blueprints
    app.register_blueprint(health_bp, url_prefix="/health")

    return app
