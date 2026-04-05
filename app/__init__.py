import logging
import time
from flask import Flask, request
from pythonjsonlogger import jsonlogger

# Peewee imports
from peewee import SqliteDatabase
from app.database import db

# CRITICAL FIX: import metrics AS A MODULE (single shared instance)
import app.routes.metrics as metrics


# Structured Logging Setup
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Console JSON logs
    console_handler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(levelname)s %(message)s"
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File logger
    try:
        file_handler = logging.FileHandler("logs/app.log")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except FileNotFoundError:
        pass


def create_app():
    setup_logging()
    app = Flask(__name__)

    # Initialize DB
    sqlite_db = SqliteDatabase("database.db")
    db.initialize(sqlite_db)
    db.connect(reuse_if_open=True)

    # Register routes AFTER DB setup
    from app.routes import register_routes
    register_routes(app)

    # Middleware: before request
    @app.before_request
    def start_timer():
        request.start_time = time.time()

    # Middleware: after request
    @app.after_request
    def log_request(response):
        latency = (time.time() - request.start_time) * 1000  # ms

        # CRITICAL: update metrics using the ONE shared module
        metrics.record_metrics(
            latency,
            is_error=(response.status_code >= 500)
        )

        # Structured logging
        app.logger.info(
            "request_complete",
            extra={
                "path": request.path,
                "method": request.method,
                "status": response.status_code,
                "latency_ms": latency,
                "client_ip": request.remote_addr,
            },
        )
        return response

    return app