import os
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import threading
from io import BytesIO
import wave
import time
from ChatGPT_API.ChatGPT_Assistant import call_ai_assistant


# Import the `variables` module to access `talking_with_chat`
try:
    import Common.variables as variables
except ImportError:
    variables = None  # Handle the case where the import fails

class KeywordDetector:
    def __init__(self, model_path, keywords, sample_rate=16000, audio_duration=1.7):
        self.model_path = model_path
        self.keywords = keywords
        self.sample_rate = sample_rate
        self.audio_duration = audio_duration
        self.model = self.load_model()
        self.running = threading.Event()
        self.threads = []  # List to track threads
        self.callback = None  # Callback function for detected keywords

    def load_model(self):
        print(f"Loading Vosk model from {self.model_path}...")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk model not found at {self.model_path}. Please ensure it is correctly unzipped.")
        model = Model(self.model_path)
        print("Model loaded successfully.")
        return model

    def keyword_detection_loop(self, id, delay=0):
        if delay > 0:
            print(f"Thread {id}: Delaying start by {delay} seconds...")
            time.sleep(delay)

        print(f"Thread {id}: Starting detection loop.")
        recognizer = KaldiRecognizer(self.model, self.sample_rate)  # Independent recognizer for each thread

        while self.running.is_set():
            if variables.talking_with_chat == False:
                try:
                    # Check if the user is currently talking with ChatGPT
                    if variables and variables.talking_with_chat:
                        print(f"Thread {id}: Paused detection (talking with ChatGPT)...")
                        time.sleep(1)  # Wait and recheck periodically
                        continue

                    # Record audio
                    audio_data = sd.rec(int(self.audio_duration * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='int16')
                    sd.wait()

                    # Create in-memory audio stream
                    audio_stream = BytesIO()
                    with wave.open(audio_stream, "wb") as wf:
                        wf.setnchannels(1)
                        wf.setsampwidth(2)
                        wf.setframerate(self.sample_rate)
                        wf.writeframes(audio_data.tobytes())

                    # Reset stream position for processing
                    audio_stream.seek(0)
                    wf = wave.open(audio_stream, "rb")

                    # Track detected keywords for this iteration
                    detected_keywords = set()

                    # Process audio with recognizer
                    while True:
                        data = wf.readframes(4000)
                        if len(data) == 0:
                            break
                        if recognizer.AcceptWaveform(data):
                            result = recognizer.Result()

                            # Parse the result for keywords (final transcription)
                            result_dict = eval(result)
                            result_text = result_dict.get("text", "").lower()

                            # Check for keywords in the final transcription
                            for keyword in self.keywords:
                                if keyword.lower() in result_text and keyword.lower() not in detected_keywords:
                                    print(f"Thread {id}: Keyword '{keyword}' detected!")
                                    detected_keywords.add(keyword.lower())  # Add to the set

                                    # Handle the keyword in the same thread
                                    if self.callback:
                                        self.callback(keyword, id)

                                    # Call AI Assistant in the same thread
                                    print(f"Thread {id}: Calling AI Assistant...")
                                    call_ai_assistant("Hey Brewsystem")  # Perform AI assistant logic here
                                    self.stop_detection()

                    # Add a delay to respect the audio duration
                    time.sleep(self.audio_duration)

                except Exception as e:
                    print(f"Thread {id}: Error in detection loop: {e}")

        print(f"Thread {id}: Exiting detection loop.")

    def start_detection(self, callback=None, threads=1, delays=None):
        if callback:
            self.callback = callback
        self.running.set()

        if delays is None:
            delays = [0] * threads  # Default: no delay for all threads

        for i in range(threads):
            thread_id = i + 1
            delay = delays[i] if i < len(delays) else 0
            thread = threading.Thread(target=self.keyword_detection_loop, args=(thread_id, delay), daemon=True)
            self.threads.append(thread)
            print(f"Starting detection thread {thread_id} with a delay of {delay} seconds...")
            thread.start()

    def stop_detection(self):
        self.running.clear()
        for thread in self.threads:
            if thread.is_alive():
                thread.join()
        print("All keyword detection threads stopped.")