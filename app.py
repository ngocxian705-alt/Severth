from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

LOGS = []

@app.route("/save", methods=["POST"])
def save():
    try:
        data = request.get_json(force=True)

        log = {
            "time": datetime.utcnow().isoformat(),
            "ip": request.headers.get("X-Forwarded-For", request.remote_addr),
            "user_agent": request.headers.get("User-Agent"),
            "data": data
        }

        LOGS.append(log)

        return jsonify(status="OK", saved=True, total=len(LOGS))

    except Exception as e:
        return jsonify(status="ERROR", msg=str(e)), 400


@app.route("/logs")
def logs():
    return jsonify(total=len(LOGS), logs=LOGS)


@app.route("/")
def home():
    return jsonify(
        name="SERVER 2 LOGGER",
        status="ONLINE",
        endpoints=["/save (POST)", "/logs (GET)"]
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)