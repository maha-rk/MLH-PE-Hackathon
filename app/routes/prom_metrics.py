from flask import Blueprint, Response
import app.routes.metrics as metrics
import psutil
import time

prom_metrics_bp = Blueprint("prom_metrics", __name__)

@prom_metrics_bp.route("/prom_metrics")
def prom_metrics():
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent
    uptime = time.time() - metrics.START_TIME

    avg_latency = (
        metrics.TOTAL_LATENCY / metrics.TOTAL_REQUESTS
        if metrics.TOTAL_REQUESTS > 0 else 0
    )
    error_rate = (
        metrics.ERROR_COUNT / metrics.TOTAL_REQUESTS
        if metrics.TOTAL_REQUESTS > 0 else 0
    )

    # Build output EXACTLY line-by-line
    lines = []
    lines.append(f"flask_app_cpu_percent {cpu}")
    lines.append(f"flask_app_memory_percent {mem}")
    lines.append(f"flask_app_uptime_seconds {uptime}")
    lines.append(f"flask_app_total_requests {metrics.TOTAL_REQUESTS}")
    lines.append(f"flask_app_error_count {metrics.ERROR_COUNT}")
    lines.append(f"flask_app_error_rate {error_rate}")
    lines.append(f"flask_app_avg_latency_ms {avg_latency}")

    body = "\n".join(lines)

    return Response(body, mimetype="text/plain")
