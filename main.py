import os
import sys
from PyQt5.QtWidgets import QApplication
from Screens.Brewscreen.brewscreen import FullScreenWindow
from ChatGPT_API.Vosk_STT import KeywordDetector
from Common.get_setting import get_setting
from Common.utils_rpi import initialize_ds18b20_resolution
from Common.constants_rpi import DS18B20_BK, DS18B20_MLT, DS18B20_HLT

def main():
    # Absolute path to the Vosk model
    model_path = os.path.join(os.path.dirname(__file__), "ChatGPT_API", "vosk-model-small-en-us-0.15")

    # Initialize the KeywordDetector with the model path and keywords from settings
    detector = KeywordDetector(
        model_path=model_path,
        keywords=get_setting("chatGPT_assistant_keywords"),
    )
    
    sensor_codes = [DS18B20_BK, DS18B20_MLT, DS18B20_HLT]

    for code in sensor_codes:
        initialize_ds18b20_resolution(code, resolution="11")

    # Start a single detection thread
    detector.start_detection()

    # Start the PyQt application
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()