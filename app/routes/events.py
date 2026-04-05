from flask import Blueprint, request, jsonify
from app.models.event import Event
from app.models.user import User
from app.models.url import URL
import json
import datetime

events_bp = Blueprint("events", __name__)

# CREATE / UPSERT EVENT — POST /events
@events_bp.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    # Required fields
    required = ["event_type", "url_id", "user_id"]
    if not data or any(k not in data for k in required):
        return jsonify({"error": "Missing fields"}), 400

    # Strict event_type validation
    if not isinstance(data["event_type"], str) or not data["event_type"].strip():
        return jsonify({"error": "Invalid event_type"}), 400

    # Strict details must be an object
    details = data.get("details", {})
    if not isinstance(details, dict):
        return jsonify({"error": "details must be an object"}), 400

    # Validate URL
    try:
        url = URL.get(URL.id == data["url_id"])
    except URL.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

    # Validate User
    try:
        user = User.get(User.id == data["user_id"])
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    # ADVANCED CHALLENGE #2:
    # "Twin’s Paradox": identical events must not create duplicates
    existing = (
        Event.select()
        .where(
            (Event.event_type == data["event_type"]) &
            (Event.url == url) &
            (Event.user == user)
        )
        .first()
    )

    if existing:
        # Update existing event (event merging)
        existing.timestamp = datetime.datetime.utcnow()
        existing.details = json.dumps(details)
        existing.save()

        return jsonify({
            "id": existing.id,
            "url_id": url.id,
            "user_id": user.id,
            "event_type": existing.event_type,
            "timestamp": existing.timestamp.isoformat(),
            "details": details
        }), 200

    # Otherwise create NEW event
    ev = Event.create(
        url=url,
        user=user,
        event_type=data["event_type"],
        timestamp=datetime.datetime.utcnow(),
        details=json.dumps(details)
    )

    return jsonify({
        "id": ev.id,
        "url_id": url.id,
        "user_id": user.id,
        "event_type": ev.event_type,
        "timestamp": ev.timestamp.isoformat(),
        "details": details
    }), 201


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

    results = []
    for e in query:
        try:
            details = json.loads(e.details) if e.details else {}
        except:
            details = {}

        results.append({
            "id": e.id,
            "url_id": e.url.id,
            "user_id": e.user.id,
            "event_type": e.event_type,
            "timestamp": e.timestamp.isoformat(),
            "details": details
        })

    return jsonify(results), 200