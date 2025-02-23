import os
import json
import threading
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer

from ChatGPT_API.ChatGPT_Assistant import call_ai_assistant, text_to_speech
from Common.utils import play_audio
from Common.detector_signals import detector_signals


# Import the variables module to access talking_with_chat
try:
    import Common.variables as variables
except ImportError:
    variables = None  # Handle the case where the import fails

class KeywordDetector:
    def __init__(self, model_path, keywords, sample_rate=16000):
        self.model_path = model_path
        self.keywords = keywords
        self.sample_rate = sample_rate
        self.model = self.load_model()
        self.running = threading.Event()
        self.thread = None
        self.callback = None
        self.ai_call_lock = threading.Lock()

    def load_model(self):
        print(f"Loading Vosk model from {self.model_path}...")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk model not found at {self.model_path}. Please ensure it is correctly unzipped.")
        model = Model(self.model_path)
        print("Model loaded successfully.")
        return model

    def detection_callback(self, indata, frames, time_info, status, recognizer):
        # If an AI conversation is in progress, skip processing
        if variables and variables.talking_with_chat:
            return

        if status:
            print(f"Status: {status}")
        # Convert the numpy array to bytes for Vosk
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
                    # Optionally call a user callback
                    if self.callback:
                        self.callback(keyword, 1)  # thread id is 1 for single-thread mode

                    # Pause further keyword detection until done talking with the assistant
                    with self.ai_call_lock:
                        if variables and not variables.talking_with_chat:
                            variables.talking_with_chat = True
                            print("Keyword detected. Calling AI Assistant...")
                            detector_signals.bruce_loading.emit()
                            play_audio("calling_Bruce - Male.mp3")
                            # Call the AI assistant inline (blocking)
                            call_ai_assistant("Hey Brewsystem", 1)
                            variables.talking_with_chat = False
                    # Once handled, break to avoid multiple triggers from the same audio block
                    break

    def keyword_detection_loop(self):
        print("Starting single-thread keyword detection loop.")
        recognizer = KaldiRecognizer(self.model, self.sample_rate)
        # Create an input stream with a callback for real-time processing
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            callback=lambda indata, frames, time_info, status: self.detection_callback(indata, frames, time_info, status, recognizer)
        ):
            # Keep the thread alive while detection is running
            while self.running.is_set():
                time.sleep(0.1)

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

    def start_voicelines_gif(self):
        gif_label_brewscreen.start_gif()