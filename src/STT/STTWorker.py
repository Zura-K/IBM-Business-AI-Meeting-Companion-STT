from PyQt5.QtCore import QThread, pyqtSignal
import logging

class STTWorker(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, processor, audio_file):
        super().__init__()
        self.processor = processor
        self.audio_file = audio_file

    def run(self):
        """Runs the speech-to-text process in a separate thread."""
        try:
            logging.info(f"Transcribing file: {self.audio_file}")
            transcription = self.processor.transcribe_audio(self.audio_file)
            self.response_signal.emit(transcription)
        except Exception as e:
            logging.error(f"Error processing audio: {e}")
            self.response_signal.emit(f"Error: {str(e)}")
