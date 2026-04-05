from flask import Blueprint, jsonify
from app.models.event import Event
import json

events_bp = Blueprint("events", __name__)

@events_bp.route("/events", methods=["GET"])
def list_events():
    events_list = []

    for ev in Event.select().order_by(Event.timestamp.desc()):
        try:
            details = json.loads(ev.details) if ev.details else {}
        except:
            details = {}

        events_list.append({
            "id": ev.id,
            "url_id": ev.url.id,
            "user_id": ev.user.id,
            "event_type": ev.event_type,
            "timestamp": ev.timestamp.isoformat(),
            "details": details
        })

    return jsonify(events_list), 200