from .health import health_bp
from .metrics import metrics_bp
from .prom_metrics import prom_metrics_bp
from .users import users_bp
from .urls import urls_bp
from .events import events_bp
from .url_shortener import url_bp   # MUST BE LAST

def register_routes(app):
    app.register_blueprint(health_bp)
    app.register_blueprint(metrics_bp)
    app.register_blueprint(prom_metrics_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(urls_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(url_bp)   # shortener always last