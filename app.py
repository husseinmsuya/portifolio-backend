from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "backend running"})

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    return jsonify({
        "success": True,
        "message": "Message received",
        "data": {
            "name": name,
            "email": email,
            "message": message
        }
    })

if __name__ == "__main__":
    app.run()