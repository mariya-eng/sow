"""
Flask backend for the Free Fire Chatbot.
Handles chat requests and communicates with the Gemini API.
"""

import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

from chatbot_config import SYSTEM_PROMPT

# Load environment variables from .env file
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Please add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name=GEMINI_MODEL,
    system_instruction=SYSTEM_PROMPT,
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"reply": "Please type a message before sending."}), 400

    try:
        response = model.generate_content(user_message)
        reply_text = response.text if response and response.text else \
            "Sorry, I couldn't generate a response. Please try again."
    except Exception:
        reply_text = "Something went wrong while contacting the AI service. Please try again later."

    return jsonify({"reply": reply_text})


if __name__ == "__main__":
    app.run(debug=True)
