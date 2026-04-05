from flask import Blueprint, request, jsonify
from app.models.event import Event
from app.models.user import User
from app.models.url import URL
import json
import datetime

events_bp = Blueprint("events", __name__)

# CREATE EVENT — POST /events
@events_bp.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "event_type" not in data or "url_id" not in data or "user_id" not in data:
        return jsonify({"error": "Missing fields"}), 400

    try:
        url = URL.get(URL.id == data["url_id"])
    except URL.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

    try:
        user = User.get(User.id == data["user_id"])
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    ev = Event.create(
        url=url,
        user=user,
        event_type=data["event_type"],
        timestamp=datetime.datetime.utcnow(),
        details=json.dumps(data.get("details", {}))
    )

    return jsonify({"id": ev.id}), 201


# LIST EVENTS — GET /events
@events_bp.route("/events", methods=["GET"])
def list_events():
    url_id = request.args.get("url_id", type=int)
    user_id = request.args.get("user_id", type=int)
    event_type = request.args.get("event_type")

    query = Event.select()

    if url_id is not None:
        query = query.where(Event.url == url_id)

    if user_id is not None:
        query = query.where(Event.user == user_id)

    if event_type is not None:
        query = query.where(Event.event_type == event_type)

    events = []
    for e in query:
        try:
            details = json.loads(e.details) if e.details else {}
        except:
            details = {}

        events.append({
            "id": e.id,
            "url_id": e.url.id,
            "user_id": e.user.id,
            "event_type": e.event_type,
            "timestamp": e.timestamp.isoformat(),
            "details": details
        })

    return jsonify(events), 200