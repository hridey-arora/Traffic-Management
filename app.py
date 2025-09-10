# app.py
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from traffic_simulation import TrafficSimulation
from signal_logic import SignalLogic
import time

app = Flask(__name__, static_folder="static")
CORS(app)

traffic = TrafficSimulation(refresh_secs=7)
logic = SignalLogic(
    cycle_time=7,
    fairness_time=90,
    pedestrian_wait=30,
    pedestrian_cross=15,
    pedestrian_cooldown=120
)
emergency_lane = None  # 0..3 or None

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/data")
def data():
    vehicles = traffic.get_vehicle_counts()
    signals = logic.decide_signals(vehicles, emergency_lane)
    current_green = next((i for i, s in enumerate(signals) if s > 0), None)

    # compute remaining seconds (backend-side)
    remaining_signals = []
    for i, s in enumerate(signals):
        if i == current_green:
            # assume logic stores start time per lane
            elapsed = int(time.time() - logic.last_green[i])
            remaining = max(s - elapsed, 0)
            remaining_signals.append(remaining)
        else:
            remaining_signals.append(0)

    ped = {
        "requested": logic.ped_requested,
        "waiting": bool(logic.ped_requested and logic.ped_request_time is not None),
    }

    return jsonify({
        "vehicles": vehicles,
        "signals": remaining_signals,   # <-- send remaining seconds
        "current_green": current_green,
        "emergency_lane": emergency_lane,
        "pedestrian": ped
    })

@app.route("/emergency", methods=["POST"])
def emergency():
    global emergency_lane
    lane = request.json.get("lane")
    if lane in [0, 1, 2, 3]:
        emergency_lane = lane
        return jsonify({"status": "ok", "emergency_lane": lane})
    return jsonify({"status": "error", "message": "lane must be 0..3"}), 400

@app.route("/clear_emergency", methods=["POST"])
def clear_emergency():
    global emergency_lane
    emergency_lane = None
    return jsonify({"status": "cleared"})

@app.route("/pedestrian", methods=["POST"])
def pedestrian():
    accepted = logic.request_pedestrian()
    return jsonify({"accepted": accepted})

if __name__ == "__main__":
    app.run(debug=True)
