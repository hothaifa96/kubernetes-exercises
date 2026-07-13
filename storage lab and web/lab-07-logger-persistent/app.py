import os
from datetime import datetime

from flask import Flask, jsonify, request

app = Flask(__name__)

LOG_DIR = os.environ.get("LOG_DIR", "/logs")
LOG_FILE = os.path.join(LOG_DIR, "application.log")

os.makedirs(LOG_DIR, exist_ok=True)

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        f.write(f"# Logger Application Started: {datetime.utcnow().isoformat()}\n")
        f.write("# Format: [TIMESTAMP] [LEVEL] MESSAGE\n")
        f.write("# " + "=" * 50 + "\n\n")

def write_log(level, message):
    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    log_entry = f"[{timestamp}] [{level}] {message}\n"
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)
    return log_entry

def read_logs(lines=100):
    if not os.path.exists(LOG_FILE):
        return []
    with open(LOG_FILE, "r") as f:
        all_lines = f.readlines()
    return all_lines[-lines:] if lines else all_lines

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "logger",
        "log_dir": LOG_DIR,
        "log_file": LOG_FILE,
        "timestamp": datetime.utcnow().isoformat()
    })

@app.route("/api/log", methods=["POST"])
def log_message():
    data = request.get_json(force=True)
    level = data.get("level", "INFO").upper()
    message = data.get("message", "")

    if not message:
        return jsonify({"error": "Message is required"}), 400

    valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    if level not in valid_levels:
        level = "INFO"

    entry = write_log(level, message)
    return jsonify({"success": True, "entry": entry.strip()})

@app.route("/api/logs", methods=["GET"])
def get_logs():
    lines = request.args.get("lines", 100, type=int)
    logs = read_logs(lines)
    return jsonify({
        "logs": [line.rstrip("\n") for line in logs],
        "count": len(logs),
        "log_file": LOG_FILE
    })

@app.route("/api/stats", methods=["GET"])
def get_stats():
    if not os.path.exists(LOG_FILE):
        return jsonify({"total_lines": 0, "file_size_bytes": 0})

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    file_size = os.path.getsize(LOG_FILE)
    
    level_counts = {}
    for line in lines:
        if "] [" in line:
            try:
                level = line.split("] [")[1].split("]")[0]
                level_counts[level] = level_counts.get(level, 0) + 1
            except:
                pass

    return jsonify({
        "total_lines": len(lines),
        "file_size_bytes": file_size,
        "level_counts": level_counts,
        "log_file": LOG_FILE
    })

@app.route("/api/clear", methods=["POST"])
def clear_logs():
    with open(LOG_FILE, "w") as f:
        f.write(f"# Logs cleared at: {datetime.utcnow().isoformat()}\n")
        f.write("# " + "=" * 50 + "\n\n")
    return jsonify({"success": True, "message": "Logs cleared"})

if __name__ == "__main__":
    print(f"Logger Application starting")
    print(f"Log directory: {LOG_DIR}")
    print(f"Log file: {LOG_FILE}")
    app.run(host="0.0.0.0", port=5000, debug=False)
