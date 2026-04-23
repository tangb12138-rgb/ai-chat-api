from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 从环境变量读取（更安全）
DIFY_API_URL = "https://api.dify.ai/v1/chat-messages"
DIFY_API_KEY = os.getenv("DIFY_API_KEY")

conversation_memory = []

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "message is required"}), 400

    conversation_memory.append({
        "role": "user",
        "content": user_message
    })

    headers = {
        "Authorization": f"Bearer {DIFY_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": {},
        "query": user_message,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "test-user"
    }

    try:
        response = requests.post(DIFY_API_URL, headers=headers, json=data)
        res_json = response.json()

        ai_reply = res_json.get("answer", "No response")

        conversation_memory.append({
            "role": "assistant",
            "content": ai_reply
        })

        return jsonify({"reply": ai_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/')
def home():
    return "API is running"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
