
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QTextCharFormat, QColor
from src.STT.SpeechDownloader import SpeechDownloader
from src.STT.STTProcessor import STTProcessor
from src.STT.STTWorker import STTWorker  # Import worker class

class STTApp(QWidget):
    """Creates a PyQt5 GUI for Speech-to-Text processing."""

    def __init__(self):
        super().__init__()

        self.downloader = SpeechDownloader(
            "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMSkillsNetwork-GPXX04C6EN/Testing%20speech%20to%20text.mp3"
        )
        self.processor = STTProcessor()
        self.worker = None  # Worker thread will be initialized later

        self.init_ui()

    def init_ui(self):
        """Initialize GUI components."""
        self.setWindowTitle("Speech-to-Text App")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        # Text display area
        self.text_display = QTextEdit()
        self.text_display.setReadOnly(True)
        layout.addWidget(self.text_display)

        # Download and Transcribe Button
        self.transcribe_button = QPushButton("Download & Transcribe")
        self.transcribe_button.clicked.connect(self.transcribe_audio)
        layout.addWidget(self.transcribe_button)

        # Upload File Button
        self.upload_button = QPushButton("Upload Audio File")
        self.upload_button.clicked.connect(self.upload_audio)
        layout.addWidget(self.upload_button)

        self.setLayout(layout)

    def transcribe_audio(self):
        """Downloads audio and transcribes it in a background thread."""
        self.text_display.clear()
        self.append_text("Downloading audio...", QColor("blue"))

        audio_file = self.downloader.download_audio()
        if not audio_file:
            self.append_text("Error: Failed to download the audio.", QColor("red"))
            return

        self.append_text("Transcribing audio...", QColor("blue"))
        self.start_transcription(audio_file)

    def upload_audio(self):
        """Allows user to upload a local audio file and transcribe it."""
        file_path, _ = QFileDialog.getOpenFileName(self, "Select an Audio File", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.append_text(f"Selected file: {file_path}", QColor("blue"))
            self.append_text("Transcribing audio...", QColor("blue"))
            self.start_transcription(file_path)

    def start_transcription(self, audio_file):
        """Starts transcription in a background thread."""
        if self.worker:
            self.worker.quit()  # Stop any running worker thread

        self.worker = STTWorker(self.processor, audio_file)
        self.worker.response_signal.connect(self.display_transcription)
        self.worker.start()

    def display_transcription(self, transcription):
        """Displays the transcribed text."""
        self.append_text(f"Transcription:\n{transcription}", QColor("green"))

    def append_text(self, text, color):
        """Appends colored text to display."""
        cursor = self.text_display.textCursor()
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        cursor.setCharFormat(fmt)
        cursor.insertText(text + "\n")
        self.text_display.setTextCursor(cursor)
        self.text_display.ensureCursorVisible()
