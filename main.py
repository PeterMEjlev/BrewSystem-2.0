import os
import sys
from PyQt5.QtWidgets import QApplication
from Screens.Brewscreen.brewscreen import FullScreenWindow
from ChatGPT_API.Vosk_STT import KeywordDetector
from Common.get_setting import get_setting

def main():
    # Absolute path to the Vosk model
    model_path = os.path.join(os.path.dirname(__file__), "ChatGPT_API", "vosk-model-small-en-us-0.15")

    # Initialize the KeywordDetector with the model path and keywords from settings
    detector = KeywordDetector(
        model_path=model_path,
        keywords=get_setting("chatGPT_assistant_keywords"),
    )

    # Start a single detection thread
    detector.start_detection()

    # Start the PyQt application
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
