"""Instâncias de extensões Flask — inicializadas sem app (init_app pattern)."""
from flask_talisman import Talisman
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()
talisman = Talisman()
