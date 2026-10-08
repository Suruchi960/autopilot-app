import os
import random
from flask import Flask, jsonify
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)

VERSION = os.getenv("APP_VERSION", "v1")
ERROR_RATE = float(os.getenv("ERROR_RATE", "0"))

REQUESTS = Counter("http_requests_total", "Total requests", ["status"])


@app.route("/")
def home():
    if random.random() < ERROR_RATE:
        REQUESTS.labels(status="500").inc()
        return jsonify(error="something broke", version=VERSION), 500
    REQUESTS.labels(status="200").inc()
    return jsonify(message="hello", version=VERSION)


@app.route("/health")
def health():
    return "ok"


@app.route("/metrics")
def metrics():
    return generate_latest(), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)