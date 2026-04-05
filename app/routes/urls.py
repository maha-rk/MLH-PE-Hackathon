from flask import Blueprint, request, jsonify, redirect
from app.models.url import URL
from app.models.user import User
from app.models.event import Event
from app.utils import generate_shortcode
import datetime
import json

urls_bp = Blueprint("urls", __name__)

# CREATE URL — POST /urls
@urls_bp.route("/urls", methods=["POST"])
def create_url():
    data = request.get_json()

    if not data or "user_id" not in data or "original_url" not in data:
        return jsonify({"error": "user_id and original_url are required"}), 400

    if not isinstance(data["user_id"], int):
        return jsonify({"error": "Invalid user_id"}), 422

    if not isinstance(data["original_url"], str):
        return jsonify({"error": "Invalid original_url"}), 422

    try:
        user = User.get(User.id == data["user_id"])
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    short = generate_shortcode()
    while URL.select().where(URL.short_code == short).exists():
        short = generate_shortcode()

    url = URL.create(
        user=user,
        short_code=short,
        original_url=data["original_url"],
        title=data.get("title"),
        is_active=True,
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow()
    )

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


# LIST URLS — GET /urls
@urls_bp.route("/urls", methods=["GET"])
def list_urls():
    user_id = request.args.get("user_id", type=int)
    is_active = request.args.get("is_active")

    query = URL.select()

    if user_id is not None:
        query = query.where(URL.user == user_id)

    if is_active is not None:
        if is_active.lower() == "true":
            query = query.where(URL.is_active == True)
        if is_active.lower() == "false":
            query = query.where(URL.is_active == False)

    urls = []
    for url in query:
        urls.append({
            "id": url.id,
            "user_id": url.user.id,
            "short_code": url.short_code,
            "original_url": url.original_url,
            "title": url.title,
            "is_active": url.is_active,
            "created_at": url.created_at.isoformat(),
            "updated_at": url.updated_at.isoformat()
        })

    return jsonify(urls), 200


# GET URL BY ID — GET /urls/<id>
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


# UPDATE URL — PUT /urls/<id>
@urls_bp.route("/urls/<int:url_id>", methods=["PUT"])
def update_url(url_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    try:
        url = URL.get(URL.id == url_id)
    except URL.DoesNotExist:
        return jsonify({"error": "URL not found"}), 404

    if "title" in data:
        if not isinstance(data["title"], str):
            return jsonify({"error": "Invalid title"}), 422
        url.title = data["title"]

    if "is_active" in data:
        if not isinstance(data["is_active"], bool):
            return jsonify({"error": "Invalid is_active"}), 422
        url.is_active = data["is_active"]

    url.updated_at = datetime.datetime.utcnow()
    url.save()

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


# REDIRECT ENDPOINT REQUIRED BY MLH TESTS
@urls_bp.route("/urls/<shortcode>/redirect", methods=["GET"])
def redirect_from_urls(shortcode):
    try:
        url = URL.get(URL.short_code == shortcode)
    except URL.DoesNotExist:
        return jsonify({"error": "Shortcode not found"}), 404

    if not url.is_active:
        return jsonify({"error": "URL is inactive"}), 410

    return redirect(url.original_url, code=302)