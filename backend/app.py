from flask import Flask, jsonify, request, send_file, Response, send_from_directory
from flask_cors import CORS
from tts_service import TTSService
from stt_service import STTService
from chat_service import ChatService
from title_service import TitleService
from voice_clone_service import VoiceCloneService
from video_service import VideoService
from text_to_image_service import TextToImageService
from supabase_service import SupabaseService

debug = False

allowed_origins = [
    "http://localhost:3000",
]

app = Flask(__name__)

CORS(app) if debug else CORS(app, origins=allowed_origins)

tts_service = TTSService()
stt_service = STTService()
chat_service = ChatService()
title_service = TitleService()
voice_clone_service = VoiceCloneService()
video_service = VideoService()
text_to_image_service = TextToImageService()
supabase_service = SupabaseService()

@app.route('/api/health')
def health():
    return jsonify({"status": "healthy"})

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()

        if not data or 'id' not in data or 'message' not in data:
            return jsonify({"error": "id and message are required"}), 400

        conversation_id = data['id']
        user_message = data['message']

        if not user_message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400

        # Get existing messages from Supabase
        existing_messages = chat_service.get_messages(conversation_id)

        # If no existing messages, start with empty list
        if existing_messages is None:
            messages = []
        else:
            messages = existing_messages

        # Add the new user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        # Get chat completion
        updated_messages = chat_service.chat_completion(messages)

        # Store updated messages back to Supabase
        chat_service.store_messages(conversation_id, updated_messages)

        return jsonify({"messages": updated_messages})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/retrieve-chat', methods=['POST'])
def retrieve_chat():
    try:
        data = request.get_json()

        if not data or 'id' not in data:
            return jsonify({"error": "id is required"}), 400

        conversation_id = data['id']

        if not conversation_id.strip():
            return jsonify({"error": "id cannot be empty"}), 400

        # Get messages from Supabase
        messages = chat_service.get_messages(conversation_id)

        if messages is None:
            return jsonify({"error": "Chat not found"}), 404

        return jsonify({"messages": messages})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-title', methods=['POST'])
def generate_title():
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400

        if 'address' not in data:
            return jsonify({"error": "Address is required"}), 400

        conversation_text = data['text']
        address = data['address']

        if not conversation_text.strip():
            return jsonify({"error": "Text cannot be empty"}), 400

        if not address.strip():
            return jsonify({"error": "Address cannot be empty"}), 400

        result = title_service.generate_conversation_title(conversation_text, address)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/list-title', methods=['POST'])
def list_title():
    try:
        data = request.get_json()

        if not data or 'address' not in data:
            return jsonify({"error": "address is required"}), 400

        address = data['address']

        if not address.strip():
            return jsonify({"error": "address cannot be empty"}), 400

        titles = title_service.list_titles_by_address(address)

        return jsonify({"titles": titles})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete-title', methods=['DELETE'])
def delete_title():
    try:
        data = request.get_json()

        if not data or 'id' not in data:
            return jsonify({"error": "id is required"}), 400

        title_id = data['id']

        if not title_id.strip():
            return jsonify({"error": "id cannot be empty"}), 400

        success = title_service.delete_title_by_id(title_id)

        if success:
            return jsonify({"message": "Title deleted successfully"})
        else:
            return jsonify({"error": "Title not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/tts', methods=['POST'])
def text_to_speech():
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "Text is required"}), 400

        text = data['text']
        voice = data.get('voice')
        voice_engine = data.get('voice_engine', 'Play3.0-mini-grpc')

        audio_buffer = tts_service.generate_audio(text, voice, voice_engine)

        return send_file(
            audio_buffer,
            mimetype='audio/mpeg',
            as_attachment=True,
            download_name='generated_audio.mp3'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/voice-clone', methods=['POST'])
def create_voice_clone():
    try:
        # Handle file upload
        if 'file' not in request.files:
            return jsonify({"error": "Audio file is required"}), 400

        audio_file = request.files['file']
        if audio_file.filename == '':
            return jsonify({"error": "No file selected"}), 400

        # Get required parameters
        address = request.form.get('address')

        if not address:
            return jsonify({"error": "address is required"}), 400

        # Create voice clone
        result = voice_clone_service.create_voice_clone(audio_file, address)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/get-voice-clone', methods=['GET'])
def get_voice_clone():
    try:
        # Get address from query parameters
        address = request.args.get('address')

        if not address:
            return jsonify({"error": "address parameter is required"}), 400

        # Get voice clone ID for the address
        voice_clone_id = voice_clone_service.get_voice_clone_id(address)

        if voice_clone_id:
            return jsonify({"address": address, "voice_clone_id": voice_clone_id})
        else:
            return jsonify({"address": address, "voice_clone_id": None, "message": "No voice clone found for this address"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/delete-voice-clone', methods=['DELETE'])
def delete_voice_clone():
    try:
        # Get address from request body
        data = request.get_json()

        if not data or 'address' not in data:
            return jsonify({"error": "address is required"}), 400

        address = data['address']

        if not address.strip():
            return jsonify({"error": "address cannot be empty"}), 400

        # Delete voice clone
        result = voice_clone_service.delete_voice_clone(address)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/stt', methods=['POST'])
def speech_to_text():
    try:
        # Handle file upload
        if 'file' in request.files:
            audio_file = request.files['file']
            if audio_file.filename == '':
                return jsonify({"error": "No file selected"}), 400

            # Get optional parameters
            response_format = request.form.get('response_format', 'json')
            language = request.form.get('language', None)
            speaker_labels = request.form.get('speaker_labels', 'false').lower() == 'true'
            prompt = request.form.get('prompt', None)

            result = stt_service.transcribe_audio(
                audio_file,
                response_format=response_format,
                language=language,
                speaker_labels=speaker_labels,
                prompt=prompt
            )

            return jsonify(result)

        # Handle URL-based transcription
        elif request.is_json:
            data = request.get_json()
            if not data or 'audio_url' not in data:
                return jsonify({"error": "Audio file or URL is required"}), 400

            audio_url = data['audio_url']
            response_format = data.get('response_format', 'json')
            language = data.get('language')
            speaker_labels = data.get('speaker_labels', False)
            prompt = data.get('prompt')

            result = stt_service.transcribe_from_url(
                audio_url,
                response_format=response_format,
                language=language,
                speaker_labels=speaker_labels,
                prompt=prompt
            )

            return jsonify(result)

        else:
            return jsonify({"error": "No audio file or URL provided"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/generate-video', methods=['POST'])
def generate_video():
    try:
        data = request.get_json()

        if not data or 'address' not in data:
            return jsonify({"error": "address is required"}), 400

        if 'request_id' not in data:
            return jsonify({"error": "request_id is required"}), 400

        if 'prompt' not in data:
            return jsonify({"error": "prompt is required"}), 400

        address = data['address']
        request_id = data['request_id']
        prompt = data['prompt']

        if not address.strip():
            return jsonify({"error": "address cannot be empty"}), 400

        if not request_id.strip():
            return jsonify({"error": "request_id cannot be empty"}), 400

        if not prompt.strip():
            return jsonify({"error": "prompt cannot be empty"}), 400

        # Generate video request
        result_request_id = video_service.generate_video(address, request_id, prompt)

        return jsonify({"request_id": result_request_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/check-generate', methods=['POST'])
def check_generate():
    try:
        data = request.get_json()

        if not data or 'address' not in data:
            return jsonify({"error": "address is required"}), 400

        address = data['address']

        if not address.strip():
            return jsonify({"error": "address cannot be empty"}), 400

        # Check video generation status
        result = video_service.check_generate(address)

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/text-to-image', methods=['POST'])
def text_to_image():
    try:
        data = request.get_json()

        if not data or 'prompt' not in data:
            return jsonify({"error": "prompt is required"}), 400

        prompt = data['prompt']
        width = data.get('width', 512)
        height = data.get('height', 512)

        if not prompt.strip():
            return jsonify({"error": "prompt cannot be empty"}), 400

        # Generate image
        result = text_to_image_service.generate_image(prompt, width, height)

        if 'error' in result:
            return jsonify({"error": result['error']}), 400

        # Return image as file
        return send_file(
            result['image'],
            mimetype='image/png',
            as_attachment=True,
            download_name=f'generated_image_{result["width"]}x{result["height"]}.png'
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0', port=5000)
