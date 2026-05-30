import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Config kutoka environment variables
GMAIL_USER = os.environ.get("GMAIL_USER")
GMAIL_PASSWORD = os.environ.get("GMAIL_PASSWORD")  # App Password, si password ya kawaida

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
        # Tengeneza email
        msg = MIMEMultipart()
        msg["From"] = GMAIL_USER
        msg["To"] = GMAIL_USER  # Unapokea kwenye email yako mwenyewe
        msg["Subject"] = f"Portfolio Contact: {name}"

        body = f"""
Ujumbe mpya kutoka portfolio yako!

Jina: {name}
Barua pepe: {email}

Ujumbe:
{message}
        """
        msg.attach(MIMEText(body, "plain"))

        # Tuma email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_USER, GMAIL_PASSWORD)
            server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())

        return jsonify({"success": True, "message": "Email imetumwa!"})

    except Exception as e:
        print(f"SMTP Kosa: {e}")
        return jsonify({"success": False, "message": "Imeshindwa kutuma email"}), 500

if __name__ == "__main__":
    app.run()