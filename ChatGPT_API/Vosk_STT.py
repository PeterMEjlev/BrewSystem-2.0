import os
import json
import threading
import time
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from io import BytesIO
import wave

from ChatGPT_API.ChatGPT_Assistant import call_ai_assistant, text_to_speech
from Common.utils import play_audio

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
        self.threads = []
        self.callback = None
        self.ai_call_lock = threading.Lock()

    def load_model(self):
        print(f"Loading Vosk model from {self.model_path}...")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk model not found at {self.model_path}. Please ensure it is correctly unzipped.")
        model = Model(self.model_path)
        print("Model loaded successfully.")
        return model

    def detection_callback(self, indata, frames, time_info, status, recognizer, thread_id):
        if status:
            print(f"Thread {thread_id} status: {status}")
        # Convert numpy array to bytes before passing it to Vosk
        audio_bytes = indata.tobytes()
        if recognizer.AcceptWaveform(audio_bytes):
            result = recognizer.Result()
            try:
                result_dict = json.loads(result)
            except Exception as e:
                print(f"Thread {thread_id}: JSON parsing error: {e}")
                return

            result_text = result_dict.get("text", "").lower()
            for keyword in self.keywords:
                if keyword.lower() in result_text:
                    # Call user-provided callback if available
                    if self.callback:
                        self.callback(keyword, thread_id)

                    with self.ai_call_lock:
                        if variables and not variables.talking_with_chat:
                            variables.talking_with_chat = True
                            print(f"Thread {thread_id}: Calling AI Assistant...")
                            play_audio("calling_Bruce - Male.mp3")
                            # Call the AI assistant inline instead of in a separate thread
                            call_ai_assistant("Hey Brewsystem", thread_id)
                            variables.talking_with_chat = False
                    # Break after handling the first recognized keyword
                    break

    def keyword_detection_loop(self, thread_id, delay=0):
        if delay > 0:
            print(f"Thread {thread_id}: Delaying start by {delay} seconds...")
            time.sleep(delay)
        print(f"Thread {thread_id}: Starting detection loop.")
        recognizer = KaldiRecognizer(self.model, self.sample_rate)

        # Create an input stream with a callback for real-time processing
        with sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            dtype='int16',
            callback=lambda indata, frames, time_info, status: self.detection_callback(indata, frames, time_info, status, recognizer, thread_id)
        ):
            # Keep the thread alive while detection is running
            while self.running.is_set():
                time.sleep(0.1)

    def start_detection(self, callback=None, threads=1, delays=None):
        """
        Starts multiple detection threads in parallel.
        
        :param callback: Optional callback function that gets called with (keyword, thread_id).
        :param threads: Number of parallel detection threads to start.
        :param delays: A list of time delays (in seconds) for each thread.
        """
        if callback:
            self.callback = callback
        self.running.set()

        if delays is None:
            delays = [0] * threads

        for i in range(threads):
            thread_id = i + 1
            delay = delays[i] if i < len(delays) else 0
            print(f"Starting detection thread {thread_id} with a delay of {delay} seconds...")
            thread = threading.Thread(
                target=self.keyword_detection_loop,
                args=(thread_id, delay),
                daemon=True
            )
            self.threads.append(thread)
            thread.start()

    def stop_detection(self):
        """Stops all detection threads."""
        self.running.clear()
        for thread in self.threads:
            thread.join()
