from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)

# 💡 Ez engedélyezi konkrétan a frontend domaint
CORS(app, origins=["https://dzsini.onlyhuman.hu"], methods=["POST", "OPTIONS"])

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return '', 200  # preflight CORS válasz

    data = request.get_json()
    prompt = data.get("message", "")

    if not prompt:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful English tutor named Dzsini."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = response.choices[0].message["content"]
        return jsonify({"reply": answer})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
