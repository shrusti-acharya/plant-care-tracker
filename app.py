from datetime import datetime, timedelta
import os
from flask import Flask, jsonify, redirect, render_template, request

app = Flask(__name__)

plants = []

COMMIT = os.getenv("RENDER_GIT_COMMIT", os.getenv("GIT_SHA", "local"))[:7]


@app.route("/")
def index():
    return render_template("index.html", plants=plants, commit=COMMIT)


@app.route("/add", methods=["POST"])
def add_plant():
    name = request.form.get("name", "").strip()
    species = request.form.get("species", "").strip()
    frequency_str = request.form.get("frequency", "").strip()
    last_watered_str = request.form.get("last_watered", "").strip()

    if not name or not species or not frequency_str or not last_watered_str:
        return "All fields are required", 400

    try:
        frequency = int(frequency_str)
        if frequency <= 0:
            raise ValueError
    except ValueError:
        return "Watering frequency must be a positive integer", 400

    try:
        last_watered_dt = datetime.strptime(last_watered_str, "%Y-%m-%d")
    except ValueError:
        return "Invalid date format. Use YYYY-MM-DD", 400

    next_due_dt = last_watered_dt + timedelta(days=frequency)
    next_due_str = next_due_dt.strftime("%Y-%m-%d")

    plant_record = {
        "id": len(plants) + 1,
        "name": name,
        "species": species,
        "frequency": frequency,
        "last_watered": last_watered_str,
        "next_due": next_due_str,
    }
    plants.append(plant_record)
    return redirect("/")


@app.route("/api/plants")
def api_plants():
    return jsonify(plants)


@app.route("/health")
def health():
    return jsonify({"status": "ok", "commit": COMMIT})


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
