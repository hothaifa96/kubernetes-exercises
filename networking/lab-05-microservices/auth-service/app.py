import os
import hmac
import hashlib
import time
from datetime import datetime, timedelta

from flask import Flask, jsonify, request

app = Flask(__name__)

AUTH_SECRET_KEY = os.environ.get("AUTH_SECRET_KEY", "default-secret-key-change-in-production")
AUTH_USER = os.environ.get("AUTH_USER", "admin")
AUTH_PASSWORD = os.environ.get("AUTH_PASSWORD", "secret")
TOKEN_EXPIRY_HOURS = int(os.environ.get("TOKEN_EXPIRY_HOURS", "24"))

_tokens = {}

def generate_token(user):
    timestamp = str(int(time.time()))
    signature = hmac.new(
        AUTH_SECRET_KEY.encode(),
        f"{user}:{timestamp}".encode(),
        hashlib.sha256
    ).hexdigest()
    token = f"{user}:{timestamp}:{signature}"
    expiry = datetime.utcnow() + timedelta(hours=TOKEN_EXPIRY_HOURS)
    _tokens[token] = {"user": user, "expiry": expiry}
    return token

def validate_token(token):
    if token not in _tokens:
        return False, None
    if _tokens[token]["expiry"] < datetime.utcnow():
        del _tokens[token]
        return False, None
    return True, _tokens[token]["user"]

@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "auth-service", "timestamp": datetime.utcnow().isoformat()})

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)
    username = data.get("username")
    password = data.get("password")

    if username == AUTH_USER and password == AUTH_PASSWORD:
        token = generate_token(username)
        return jsonify({"success": True, "token": token, "user": username})
    else:
        return jsonify({"success": False, "error": "Invalid credentials"}), 401

@app.route("/validate", methods=["POST"])
def validate():
    data = request.get_json(force=True)
    token = data.get("token")

    valid, user = validate_token(token)
    if valid:
        return jsonify({"valid": True, "user": user})
    else:
        return jsonify({"valid": False, "error": "Invalid or expired token"}), 401

if __name__ == "__main__":
    print(f"Auth Service starting — User: {AUTH_USER}")
    print(f"Token expiry: {TOKEN_EXPIRY_HOURS} hours")
    app.run(host="0.0.0.0", port=5001, debug=False)
