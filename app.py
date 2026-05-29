from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/contact", methods=["POST"])
def contact():
    data = request.json

    name = data.get("name")
    email = data.get("email")
    message = data.get("message")

    return jsonify({
        "success": True,
        "message": "Message received"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)