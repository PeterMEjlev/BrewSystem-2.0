import os
import sys
from PyQt5.QtWidgets import QApplication
from Screens.Brewscreen.brewscreen import FullScreenWindow
from ChatGPT_API.Vosk_STT import KeywordDetector
from Common.get_setting import get_setting

def handle_keyword(keyword, thread_id):
    """
    Callback function to handle detected keywords.
    """
    print(f"Thread {thread_id}: Detected keyword: {keyword}")
    # Perform actions here, like updating the GUI or triggering events.

def main():
    # Absolute path to the Vosk model
    model_path = os.path.join(os.path.dirname(__file__), "ChatGPT_API", "vosk-model-small-en-us-0.15")

    keywords = get_setting("chatGPT_assistant_keywords")

    # Initialize the KeywordDetector
    detector = KeywordDetector(
        model_path=model_path,  # Provide the absolute path
        keywords=keywords,
    )

    # Start two detection threads directly
    detector.start_detection(callback=handle_keyword, threads=2, delays=[0, 0.5])

    # Start the PyQt application
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
