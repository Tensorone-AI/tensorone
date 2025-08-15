import requests
import io
from typing import Optional, Dict, Any


class STTService:
    def __init__(self):
        self.api_key = "API_KEY"
        self.base_url = "https://api.lemonfox.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def transcribe_audio(self, audio_file, response_format: str = "json",
                        language: Optional[str] = None,
                        speaker_labels: bool = False,
                        prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio file using LemonFox API

        Args:
            audio_file: Audio file buffer or file path
            response_format: Response format (json, text, srt, verbose_json, vtt)
            language: Language code for transcription (auto-detected if None)
            speaker_labels: Enable speaker diarization
            prompt: Optional prompt to guide transcription style

        Returns:
            Dictionary containing transcription result
        """
        url = f"{self.base_url}/audio/transcriptions"

        # Prepare form data
        data = {
            "response_format": response_format,
            "speaker_labels": speaker_labels
        }

        if language:
            data["language"] = language
        if prompt:
            data["prompt"] = prompt

        # Handle file upload
        if isinstance(audio_file, io.BytesIO):
            files = {"file": ("audio.mp3", audio_file, "audio/mpeg")}
        else:
            files = {"file": audio_file}

        # Remove Content-Type header for multipart/form-data
        headers = {"Authorization": f"Bearer {self.api_key}"}

        response = requests.post(url, data=data, files=files, headers=headers)

        if response.status_code == 200:
            if response_format == "json" or response_format == "verbose_json":
                return response.json()
            else:
                return {"text": response.text, "status": "success"}
        else:
            raise Exception(f"STT API error: {response.status_code} - {response.text}")

    def transcribe_from_url(self, audio_url: str, response_format: str = "json",
                           language: Optional[str] = None,
                           speaker_labels: bool = False,
                           prompt: Optional[str] = None) -> Dict[str, Any]:
        """
        Transcribe audio from URL using LemonFox API

        Args:
            audio_url: URL of the audio file to transcribe
            response_format: Response format (json, text, srt, verbose_json, vtt)
            language: Language code for transcription (auto-detected if None)
            speaker_labels: Enable speaker diarization
            prompt: Optional prompt to guide transcription style

        Returns:
            Dictionary containing transcription result
        """
        url = f"{self.base_url}/audio/transcriptions"

        data = {
            "file": audio_url,
            "response_format": response_format,
            "speaker_labels": speaker_labels
        }

        if language:
            data["language"] = language
        if prompt:
            data["prompt"] = prompt

        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 200:
            if response_format == "json" or response_format == "verbose_json":
                return response.json()
            else:
                return {"text": response.text}
        else:
            raise Exception(f"STT API error: {response.status_code} - {response.text}")
