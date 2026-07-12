import os
import hmac
import hashlib
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", "default-secret-key-change-in-production")

_items = [
    {"id": "1", "name": "Alpha", "value": "First item"},
    {"id": "2", "name": "Beta", "value": "Second item"},
    {"id": "3", "name": "Gamma", "value": "Third item"},
]

def validate_token(token):
    parts = token.split(":")
    if len(parts) != 3:
        return False
    user, timestamp, signature = parts
    expected = hmac.new(
        AUTH_SECRET_KEY.encode(),
        f"{user}:{timestamp}".encode(),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(signature, expected)

@app.before_request
def check_auth():
    if request.endpoint == "health":
        return
    if request.method == "OPTIONS":
        return

    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token or not validate_token(token):
        return jsonify({"error": "Unauthorized"}), 401

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "data-service", "timestamp": datetime.utcnow().isoformat()})

@app.route("/items", methods=["GET"])
def get_items():
    return jsonify({"items": _items})

@app.route("/items", methods=["POST"])
def create_item():
    data = request.get_json(force=True)
    name = data.get("name")
    value = data.get("value")

    if not name or not value:
        return jsonify({"error": "Name and value required"}), 400

    new_id = str(len(_items) + 1)
    new_item = {"id": new_id, "name": name, "value": value}
    _items.append(new_item)
    return jsonify({"success": True, "item": new_item})

@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    global _items
    original_len = len(_items)
    _items = [item for item in _items if item["id"] != item_id]
    if len(_items) == original_len:
        return jsonify({"error": "Item not found"}), 404
    return jsonify({"success": True, "deleted": item_id})

if __name__ == "__main__":
    print(f"Data Service starting — {len(_items)} items loaded")
    app.run(host="0.0.0.0", port=5002, debug=False)
