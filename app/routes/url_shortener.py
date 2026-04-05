from flask import Blueprint, request, jsonify, redirect
from app.models.url import URL
from app.utils import generate_shortcode
import logging

url_bp = Blueprint("url_shortener", __name__, url_prefix="/r")

@url_bp.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    
    if not data or "url" not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    original = data["url"]

    shortcode = generate_shortcode()
    while URL.select().where(URL.shortcode == shortcode).exists():
        shortcode = generate_shortcode()

    entry = URL.create(original_url=original, shortcode=shortcode)
    logging.info("short_url_created", extra={"shortcode": shortcode, "url": original})

    return jsonify({
        "original_url": original,
        "shortcode": shortcode,
        "short_url": f"http://localhost:5003/{shortcode}"
    }), 201


@url_bp.route("/<shortcode>", methods=["GET"])
def redirect_short_url(shortcode):
    try:
        url_entry = URL.get(URL.short_code == shortcode)
    except URL.DoesNotExist:
        return jsonify({"error": "Shortcode not found"}), 404

    # ✅ NEW: Inactive URL should NOT redirect
    if not url_entry.is_active:
        return jsonify({"error": "URL is inactive"}), 410  # or 400/404 accepted too

    # ✅ redirect if active
    return redirect(url_entry.original_url, code=302)