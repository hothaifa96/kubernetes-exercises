import os
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

app = Flask(__name__)
CORS(app)

POD_NAME = os.environ.get("POD_NAME", "unknown-pod")
POD_IP = os.environ.get("POD_IP", "unknown-ip")
MONGO_URI = f'mongodb://{os.environ.get("DB_USER","mongo")}:{os.environ.get("DB_PASSWORD","mongo")}@{os.environ.get("DB_HOST", "localhost")}:27017'
# mongodb://username:password@host:port/databaseName
DB_NAME = os.environ.get("DB_NAME", "pizzadb")

PIZZAS = [
    {"id": 1, "name": "Margherita",     "price": 8.99,  "emoji": "🍕", "description": "Classic tomato sauce and fresh mozzarella"},
    {"id": 2, "name": "Pepperoni",      "price": 10.99, "emoji": "🍖", "description": "Loaded with spicy pepperoni slices"},
    {"id": 3, "name": "BBQ Chicken",    "price": 12.99, "emoji": "🍗", "description": "Smoky BBQ sauce with grilled chicken"},
    {"id": 4, "name": "Veggie Supreme", "price": 9.99,  "emoji": "🥦", "description": "Bell peppers, mushrooms, olives, onions"},
    {"id": 5, "name": "Four Cheese",    "price": 11.99, "emoji": "🧀", "description": "Mozzarella, cheddar, gouda and parmesan"},
    {"id": 6, "name": "Diavola",        "price": 13.49, "emoji": "🌶️", "description": "Spicy salami and chilli flakes"},
]

_mongo_client = None


def get_db():
    global _mongo_client
    try:
        if _mongo_client is None:
            _mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
        _mongo_client.admin.command("ping")
        return _mongo_client[DB_NAME], True
    except (ConnectionFailure, ServerSelectionTimeoutError, Exception):
        _mongo_client = None
        return None, False


@app.route("/health")
def health():
    return jsonify({"status": "ok", "pod_name": POD_NAME, "pod_ip": POD_IP})


@app.route("/api/info")
def info():
    _, db_connected = get_db()
    safe_uri = MONGO_URI.split("@")[-1] if "@" in MONGO_URI else MONGO_URI
    return jsonify({
        "pod_name": POD_NAME,
        "pod_ip": POD_IP,
        "db_connected": db_connected,
        "db_uri": safe_uri,
    })


@app.route("/api/pizzas")
def get_pizzas():
    return jsonify({"pizzas": PIZZAS, "served_by_pod": POD_NAME, "served_by_ip": POD_IP})


@app.route("/api/order", methods=["POST"])
def place_order():
    data = request.get_json(force=True)
    pizza_id = data.get("pizza_id")
    customer = data.get("customer", "Anonymous").strip() or "Anonymous"

    pizza = next((p for p in PIZZAS if p["id"] == pizza_id), None)
    if not pizza:
        return jsonify({"error": "Pizza not found"}), 404

    order = {
        "pizza_name": pizza["name"],
        "pizza_emoji": pizza["emoji"],
        "customer": customer,
        "price": pizza["price"],
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "served_by_pod": POD_NAME,
        "served_by_ip": POD_IP,
    }

    db, db_connected = get_db()
    if db_connected:
        result = db.orders.insert_one(order)
        order.pop("_id", None)
        order["saved_to_db"] = True
    else:
        order["saved_to_db"] = False

    return jsonify({"success": True, "order": order})


@app.route("/api/orders")
def get_orders():
    db, db_connected = get_db()
    if not db_connected:
        return jsonify({"orders": [], "db_connected": False, "served_by_pod": POD_NAME})

    orders = list(
        db.orders.find({}, {"_id": 0}).sort("timestamp", -1).limit(20)
    )
    return jsonify({"orders": orders, "db_connected": True, "served_by_pod": POD_NAME})


if __name__ == "__main__":
    print(f"Pizza Backend starting — Pod: {POD_NAME} / IP: {POD_IP}")
    print(f"MongoDB URI: {MONGO_URI}")
    app.run(host="0.0.0.0", port=5000, debug=False)
