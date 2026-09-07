import os
import sys

from flask import Flask, jsonify, render_template

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.access_log import read_events  # noqa: E402

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/events")
def api_events():
    events = sorted(read_events(), key=lambda e: e["timestamp"], reverse=True)
    return jsonify(events[:500])


@app.route("/api/stats")
def api_stats():
    events = read_events()
    by_method = {}
    for e in events:
        if e["event"] == "access_granted":
            by_method[e["method"]] = by_method.get(e["method"], 0) + 1

    stats = {
        "total_granted": sum(1 for e in events if e["event"] == "access_granted"),
        "total_denied": sum(1 for e in events if e["event"] == "access_denied"),
        "entries": sum(1 for e in events if e["event"] == "door_open"),
        "exits": sum(1 for e in events if e["event"] == "door_close"),
        "by_method": by_method,
    }
    return jsonify(stats)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
