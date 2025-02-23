import os
import json
import threading
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from Common.config import IS_RPI
from ChatGPT_API.ChatGPT_Assistant import call_ai_assistant, text_to_speech
from Common.utils import play_audio
from Common.detector_signals import detector_signals

try:
    import Common.variables as variables
except ImportError:
    variables = None

class KeywordDetector:
    def __init__(self, model_path, keywords, sample_rate=44100):
        self.model_path = model_path
        self.keywords = keywords
        self.sample_rate = sample_rate
        self.model = self.load_model()
        self.running = threading.Event()
        self.running.set()
        self.thread = None
        self.callback = None
        self.keyword_detected = threading.Event()  # flag for keyword detection
        self.detected_keyword = None  # to store which keyword was detected
        self.ai_call_lock = threading.Lock()

    def load_model(self):
        print(f"Loading Vosk model from {self.model_path}...")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk model not found at {self.model_path}. Please ensure it is correctly unzipped.")
        model = Model(self.model_path)
        print("Model loaded successfully.")
        return model

    def detection_callback(self, indata, frames, time_info, status, recognizer):
        if variables and variables.talking_with_chat:
            return

        if status:
            print(f"Status: {status}")

        audio_bytes = indata.tobytes()
        if recognizer.AcceptWaveform(audio_bytes):
            result = recognizer.Result()
            try:
                result_dict = json.loads(result)
            except Exception as e:
                print(f"JSON parsing error: {e}")
                return

            result_text = result_dict.get("text", "").lower()
            for keyword in self.keywords:
                if keyword.lower() in result_text:
                    # Optionally call a user callback in a thread-safe way
                    if self.callback:
                        self.callback(keyword, 1)
                    self.detected_keyword = keyword
                    self.keyword_detected.set()
                    # Break to avoid multiple triggers from the same audio block
                    break

    def keyword_detection_loop(self):
        while self.running.is_set():
            print("Starting detection cycle.")
            recognizer = KaldiRecognizer(self.model, self.sample_rate)

            def stream_callback(indata, frames, time_info, status):
                self.detection_callback(indata, frames, time_info, status, recognizer)

            stream_kwargs = {
                "samplerate": self.sample_rate,
                "channels": 1,
                "dtype": 'int16',
                "callback": stream_callback
            }
            if IS_RPI:
                stream_kwargs["device"] = 2

            # Open the audio stream for this cycle
            with sd.InputStream(**stream_kwargs):
                # Run until a keyword is detected (or detection is stopped)
                while self.running.is_set() and not self.keyword_detected.is_set():
                    time.sleep(0.1)

            # At this point, the stream is closed so the microphone is freed.
            if self.keyword_detected.is_set():
                with self.ai_call_lock:
                    if variables and not variables.talking_with_chat:
                        variables.talking_with_chat = True
                        print("Keyword detected. Calling AI Assistant...")
                        detector_signals.bruce_loading.emit()
                        play_audio("calling_Bruce - Male.mp3")
                        call_ai_assistant("Hey Brewsystem", 1)
                        variables.talking_with_chat = False

                # Reset the flag to allow future detection cycles.
                self.keyword_detected.clear()
            # Optionally, add a short sleep to avoid a rapid restart
            time.sleep(0.2)


    def start_detection(self, callback=None):
        """
        Starts the keyword detection loop on a single thread.
        
        :param callback: Optional callback function that gets called with (keyword, thread_id).
        """
        if callback:
            self.callback = callback
        self.running.set()
        self.thread = threading.Thread(target=self.keyword_detection_loop, daemon=True)
        self.thread.start()

    def stop_detection(self):
        """Stops the detection thread."""
        self.running.clear()
        if self.thread:
            self.thread.join()
