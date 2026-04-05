from flask import Blueprint, request, jsonify
from app.models.user import User
import datetime
import csv
from io import TextIOWrapper

users_bp = Blueprint("users", __name__)

# ✅ CREATE USER — POST /users
@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "username" not in data or "email" not in data:
        return jsonify({"error": "username and email required"}), 400

    if not isinstance(data["username"], str) or not isinstance(data["email"], str):
        return jsonify({"error": "Invalid field types"}), 422

    user = User.create(
        username=data["username"],
        email=data["email"],
        created_at=datetime.datetime.utcnow()
    )

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 201


# ✅ LIST USERS — GET /users
@users_bp.route("/users", methods=["GET"])
def list_users():
    page = request.args.get("page", type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=1000)

    query = User.select().paginate(page, per_page)

    users_list = []
    for user in query:
        users_list.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "created_at": user.created_at.isoformat()
        })

    return jsonify(users_list), 200


# ✅ GET USER BY ID — GET /users/<id>
@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    try:
        user = User.get(User.id == user_id)
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200


# ✅ UPDATE USER — PUT /users/<id>
@users_bp.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "Request body required"}), 400

    try:
        user = User.get(User.id == user_id)
    except User.DoesNotExist:
        return jsonify({"error": "User not found"}), 404

    if "username" in data:
        if not isinstance(data["username"], str):
            return jsonify({"error": "Invalid username"}), 422
        user.username = data["username"]

    if "email" in data:
        if not isinstance(data["email"], str):
            return jsonify({"error": "Invalid email"}), 422
        user.email = data["email"]

    user.save()

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "created_at": user.created_at.isoformat()
    }), 200


# ✅ BULK IMPORT — POST /users/bulk
@users_bp.route("/users/bulk", methods=["POST"])
def bulk_import_users():
    if "file" not in request.files:
        return jsonify({"error": "CSV file required"}), 400

    file = request.files["file"]

    # ✅ Read CSV file in text mode
    csv_file = TextIOWrapper(file, encoding="utf-8")
    reader = csv.DictReader(csv_file)

    imported = 0

    for row in reader:
        # Required columns: username, email
        if "username" not in row or "email" not in row:
            continue

        # Create user
        User.create(
            username=row["username"],
            email=row["email"],
            created_at=datetime.datetime.utcnow()
        )
        imported += 1

    return jsonify({"count": imported}), 200