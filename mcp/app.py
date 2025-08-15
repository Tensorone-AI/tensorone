from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import asyncio
from agentic_chat_service import AgenticChatService

debug = False

allowed_origins = [
    "http://localhost:3000",
]

app = Flask(__name__)

CORS(app) if debug else CORS(app, origins=allowed_origins)

agentic_chat_service = AgenticChatService()

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/agentic-chat', methods=['POST'])
def agentic_chat():
    try:
        data = request.get_json()

        if not data or 'messages' not in data or 'slug' not in data:
            return jsonify({"error": "Messages array and slug are required"}), 400

        messages = data['messages']
        slug = data['slug']
        call = data.get('call', False)

        if not isinstance(messages, list):
            return jsonify({"error": "Messages must be an array"}), 400

        if not isinstance(slug, str) or not slug.strip():
            return jsonify({"error": "Slug must be a non-empty string"}), 400

        if not isinstance(call, bool):
            return jsonify({"error": "Call parameter must be a boolean"}), 400

        # Validate message format
        for message in messages:
            if not isinstance(message, dict) or 'role' not in message or 'content' not in message:
                return jsonify({"error": "Each message must have 'role' and 'content' fields"}), 400

        # Get agentic chat completion with optional audio enhancement
        result = asyncio.run(agentic_chat_service.agentic_chat_completion(messages, slug.strip(), call))

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0', port=5000)
