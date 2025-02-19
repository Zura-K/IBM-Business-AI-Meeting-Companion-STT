import torch
from transformers import pipeline

class STTProcessor:
    """Handles speech-to-text conversion using OpenAI Whisper."""

    def __init__(self, model_name="openai/whisper-tiny.en"):
        self.model_name = model_name
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=self.model_name,
            chunk_length_s=30,
        )

    def transcribe_audio(self, audio_file_path):
        if not audio_file_path:
            return "No valid audio file provided."
        prediction = self.pipe(audio_file_path)["text"]
        return prediction
