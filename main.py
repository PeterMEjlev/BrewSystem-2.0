import os, threading, sys
from zeroconf import Zeroconf
from PyQt5.QtWidgets import QApplication
from Webpage.network_helpers import run_flask_app, register_mdns
from Screens.Brewscreen.brewscreen import FullScreenWindow
from ChatGPT_API.Vosk_STT import KeywordDetector
from Common.get_setting import get_setting
from Common.utils_rpi import initialize_ds18b20_resolution
from Common.constants_rpi import DS18B20_BK, DS18B20_MLT, DS18B20_HLT
from Webpage.app import app as flask_app  

def main():
    # paths to STT model and ChatGPT API
    model_path = os.path.join(os.path.dirname(__file__),
                              "ChatGPT_API", "vosk-model-small-en-us-0.15")
    
    # init sensors
    for code in (DS18B20_BK, DS18B20_MLT, DS18B20_HLT):
        initialize_ds18b20_resolution(code, resolution="11")

    # start voice detector
    detector = KeywordDetector(model_path=model_path,
                               keywords=get_setting("chatGPT_assistant_keywords"))
    detector.start_detection()

    # start GUI
    app = QApplication(sys.argv)
    window = FullScreenWindow()
    
    # mDNS advertise & start Flask
    zeroconf: Zeroconf = register_mdns("brewsystem", 5000)
    flask_thread = threading.Thread(
        target=run_flask_app, args=(flask_app,), daemon=True
    )
    flask_thread.start()

    try:
        sys.exit(app.exec_())
    finally:
        zeroconf.unregister_all_services()
        zeroconf.close()

if __name__ == "__main__":
    main()
