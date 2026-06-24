from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.get("")
def health_check():
    """Retorna status da API."""
    return jsonify({"status": "ok"})
