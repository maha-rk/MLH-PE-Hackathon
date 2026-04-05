from flask import Blueprint, request, jsonify
from app.models.url import URL
from app.models.user import User
from app.utils import generate_shortcode
import datetime
import json
from app.models.event import Event

urls_bp = Blueprint("urls", __name__)

# ✅ CREATE URL — POST /urls
@urls_bp.route("/urls", methods=["POST"])
def create_url():
    data = request.get_json()

    # ✅ Validate required fields
    if not data or "user_id" not in data or "original_url" not in data:
        return jsonify({"error": "user_id and original_url are required"}), 400

    # ✅ Type validation
    if not isinstance(data["user_id"], int):
        return jsonify({"error": "Invalid user_id"}), 422
    if not isinstance(data["original_url"], str):
        return jsonify({"error": "Invalid original_url"}), 422

    # ✅ Validate user exists
    try:
        user = User.get(User.id == data["user_id"])
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    # ✅ Unique shortcode
    short = generate_shortcode()
    while URL.select().where(URL.short_code == short).exists():
        short = generate_shortcode()

    # ✅ Create URL
    url = URL.create(
        user=user,
        short_code=short,
        original_url=data["original_url"],
        title=data.get("title"),
        is_active=True,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )

    # ✅ Log event: created
    Event.create(
        url=url,
        user=user,
        event_type="created",
        details=json.dumps({
            "short_code": url.short_code,
            "original_url": url.original_url
        })
    )

    return jsonify({
        "id": url.id,
        "user_id": url.user.id,
        "short_code": url.short_code,
        "original_url": url.original_url,
        "title": url.title,
        "is_active": url.is_active,
        "created_at": url.created_at.isoformat(),
        "updated_at": url.updated_at.isoformat()
    }), 201


# ✅ LIST URLS — GET /urls
@urls_bp.route("/urls", methods=["GET"])
def list_urls():
    user_filter = request.args.get("user_id", type=int)

    if user_filter:
        query = URL.select().where(URL.user == user_filter)
    else:
        query = URL.select()

    urls_list = []
    for url in query:
        urls_list.append({
            "id": url.id,
            "user_id": url.user.id,
            "short_code": url.short_code,
            "original_url": url.original_url,
            "title": url.title,
            "is_active": url.is_active,
            "created_at": url.created_at.isoformat(),
            "updated_at": url.updated_at.isoformat()
        })

    return jsonify(urls_list), 200


# ✅ GET URL BY ID — GET /urls/<id>
@urls_bp.route("/urls/<int:url_id>", methods=["GET"])
def get_url(url_id):
    try:
        url = URL.get(URL.id == url_id)
    except URL.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

    return jsonify({
        "id": url.id,
        "user_id": url.user.id,
        "short_code": url.short_code,
        "original_url": url.original_url,
        "title": url.title,
        "is_active": url.is_active,
        "created_at": url.created_at.isoformat(),
        "updated_at": url.updated_at.isoformat()
    }), 200


# ✅ UPDATE URL — PUT /urls/<id>
@urls_bp.route("/urls/<int:url_id>", methods=["PUT"])
def update_url(url_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body required"}), 400

    # ✅ Find URL
    try:
        url = URL.get(URL.id == url_id)
    except URL.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

    # ✅ Validate fields
    if "title" in data and not isinstance(data["title"], str):
        return jsonify({"error": "Invalid title"}), 422

    if "is_active" in data and not isinstance(data["is_active"], bool):
        return jsonify({"error": "Invalid is_active"}), 422

    # ✅ Update fields
    if "title" in data:
        url.title = data["title"]

    if "is_active" in data:
        url.is_active = data["is_active"]

    url.updated_at = datetime.datetime.utcnow()
    url.save()

    # ✅ Log event: updated
    Event.create(
        url=url,
        user=url.user,
        event_type="updated",
        details=json.dumps({
            "short_code": url.short_code,
            "title": url.title,
            "is_active": url.is_active
        })
    )

    return jsonify({
        "id": url.id,
        "user_id": url.user.id,
        "short_code": url.short_code,
        "original_url": url.original_url,
        "title": url.title,
        "is_active": url.is_active,
        "created_at": url.created_at.isoformat(),
        "updated_at": url.updated_at.isoformat()
    }), 200