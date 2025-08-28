from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

TARGET_TIME = "06:45"

def calculate_time(distance_km):
    distance_m = distance_km * 1000
    v_min, v_max = 1, 10  # m/s

    # Δt for v=1 and v=10
    t_min = distance_m / v_min  # in seconds
    t_max = distance_m / v_max

    # convert seconds → minutes
    t_min_min = t_min / 60
    t_max_min = t_max / 60

    # target time
    target = datetime.strptime(TARGET_TIME, "%H:%M")

    # earliest departure = target - larger time (slower speed)
    earliest = target - timedelta(minutes=t_min_min)
    # latest departure = target - smaller time (faster speed)
    latest = target - timedelta(minutes=t_max_min)

    return earliest.strftime("%H:%M"), latest.strftime("%H:%M")

@app.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    distance = float(data["distance"])
    earliest, latest = calculate_time(distance)
    return jsonify({"earliest": earliest, "latest": latest})

if __name__ == "__main__":
    app.run(debug=True)