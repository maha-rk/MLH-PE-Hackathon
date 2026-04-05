from flask import Blueprint, jsonify
from app.alerts import send_email_alert
from app.routes.metrics import high_error_rate

health_bp = Blueprint("health", __name__)

@health_bp.route("/health")
def health():
    try:
        # ✅ Uncomment this line during FIRE DRILL
        # raise Exception("Simulated failure for Incident Response")

        # ✅ Optional: trigger alert for high error rate
        if high_error_rate():
            send_email_alert(
                "High Error Rate",
                "Error rate exceeded 30% of recent requests."
            )

        return jsonify({"status": "ok"}), 200

    except Exception as e:
        # ✅ Alert for service down
        send_email_alert("Service DOWN", f"Health check failed: {e}")
        return jsonify({"error": "service unavailable"}), 503