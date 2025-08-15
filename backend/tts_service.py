from pyht import Client
from pyht.client import TTSOptions, Format
import io


class TTSService:
    def __init__(self):
        self.client = Client(
            user_id="USER_ID",
            api_key="API_KEY"
        )

    def generate_audio(self, text, voice=None, voice_engine='Play3.0-mini-grpc'):
        if voice is None:
            voice = 's3://voice-cloning-zero-shot/775ae416-49bb-4fb6-bd45-740f205d20a1/jennifersaad/manifest.json'

        options = TTSOptions(voice=voice, format=Format.FORMAT_MP3)
        audio_buffer = io.BytesIO()

        for chunk in self.client.tts(text, options, voice_engine=voice_engine):
            audio_buffer.write(chunk)

        audio_buffer.seek(0)
        return audio_buffer
