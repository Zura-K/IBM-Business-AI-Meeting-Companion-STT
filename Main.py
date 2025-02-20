import sys
import logging

# First, setup the virtual environment before importing anything else
from Venv import VirtualEnvironment  # Import Venv first

venv = VirtualEnvironment()
venv.setup_and_run()  # Ensure the virtual environment is ready

# Now that the virtual environment is set up, import dependencies
from PyQt5.QtWidgets import QApplication
from src.STT.STTApp import STTApp

def main():
    """Entry point for the application."""
    try:
        logging.info("Starting Speech-to-Text Application...")

        app = QApplication(sys.argv)
        window = STTApp()
        window.show()
        logging.info("Application started successfully.")
        sys.exit(app.exec_())
    except Exception as e:
        logging.error(f"Application Error: {e}")

if __name__ == "__main__":
    main()
