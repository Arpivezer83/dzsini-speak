from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import openai
import os
import traceback

app = Flask(__name__)
CORS(app)  # globális engedélyezés fallbackként

openai.api_key = os.getenv("OPENAI_API_KEY")
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        message = data.get("message", "")
        response = get_openai_response(message)
        return jsonify({"response": response})
    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
