from flask import Blueprint, jsonify
import app.routes.metrics as metrics
import psutil, time

metrics_bp = Blueprint("metrics", __name__)

START_TIME = time.time()

# THESE ARE GLOBAL COUNTERS
TOTAL_REQUESTS = 0
ERROR_COUNT = 0
TOTAL_LATENCY = 0.0


def record_metrics(latency_ms: float, is_error: bool = False):
    """
    This function MUST update counters for EVERY request.
    """
    global TOTAL_REQUESTS, ERROR_COUNT, TOTAL_LATENCY

    TOTAL_REQUESTS += 1
    TOTAL_LATENCY += latency_ms

    if is_error:
        ERROR_COUNT += 1


def high_error_rate():
    if TOTAL_REQUESTS < 10:
        return False
    return (ERROR_COUNT / TOTAL_REQUESTS) > 0.3


@metrics_bp.route("/metrics")
def metrics():
    uptime = time.time() - START_TIME
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    avg_latency = TOTAL_LATENCY / TOTAL_REQUESTS if TOTAL_REQUESTS else 0
    error_rate = ERROR_COUNT / TOTAL_REQUESTS if TOTAL_REQUESTS else 0

    return jsonify({
        "cpu_percent": cpu,
        "memory_percent": mem,
        "uptime_seconds": uptime,
        "total_requests": TOTAL_REQUESTS,
        "error_count": ERROR_COUNT,
        "error_rate": error_rate,
        "avg_latency_ms": avg_latency
    })
