from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from openai import OpenAI  # új import
import os
from dotenv import load_dotenv

# Környezeti változók betöltése
load_dotenv()

# OpenAI kliens inicializálása
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# Flask app beállítás
app = Flask(__name__)
CORS(app)

# Rate limiting (pl. 10 kérés percenként IP-címenként)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["10 per minute"]
)

# Home (statikus HTML betöltése)
@app.route("/")
def home():
    return render_template("index.html")

# Chat endpoint
@app.route("/chat", methods=["POST"])
@limiter.limit("5 per minute")  # Egyedi limit is lehet
def chat():
    # Egyszerű jogosultságkezelés (opcionális fejlesztés alatt)
    auth_token = request.headers.get("Authorization")
    if auth_token != "Bearer my-secret-token":
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    user_input = data.get("message", "")

    # Input validálás
    if not user_input or len(user_input) > 200:
        return jsonify({"error": "Invalid input"}), 400

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an encouraging and friendly English tutor."},
                {"role": "user", "content": user_input}
            ]
        )
        reply = response.choices[0].message.content
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Futás helyben
if __name__ == "__main__":
    app.run(debug=True)
