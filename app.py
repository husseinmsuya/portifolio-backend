import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=[
    "https://portifolio-frontend-d8s6.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000"
])

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
MAIL_TO = os.environ.get("MAIL_TO")

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "backend running"})

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    if not all([name, email, message]):
        return jsonify({"success": False, "message": "Taarifa zote zinahitajika"}), 400

    try:
        response = requests.post(
            "https://api.resend.com/emails",
            headers={
                "Authorization": f"Bearer {RESEND_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "from": "onboarding@resend.dev",
                "to": MAIL_TO,
                "subject": f"Portfolio Contact: {name}",
                "text": f"Jina: {name}\nBarua pepe: {email}\n\nUjumbe:\n{message}"
            }
        )

        if response.status_code == 200:
            return jsonify({"success": True, "message": "Email imetumwa!"})
        else:
            print(f"Resend error: {response.text}")
            return jsonify({"success": False, "message": "Imeshindwa kutuma"}), 500

    except Exception as e:
        print(f"Kosa: {e}")
        return jsonify({"success": False, "message": "Imeshindwa kutuma email"}), 500

if __name__ == "__main__":
    app.run()