import os
from vosk import Model, KaldiRecognizer
import sounddevice as sd
import threading
from io import BytesIO
import wave
import time
from ChatGPT_API.ChatGPT_Assistant import call_ai_assistant, text_to_speech

# Import the `variables` module to access `talking_with_chat`
try:
    import Common.variables as variables
except ImportError:
    variables = None  # Handle the case where the import fails


class KeywordDetector:
    def __init__(self, model_path, keywords, sample_rate=16000, audio_duration=1):
        self.model_path = model_path
        self.keywords = keywords
        self.sample_rate = sample_rate
        self.audio_duration = audio_duration
        self.model = self.load_model()
        
        # Event to control the run state of the threads
        self.running = threading.Event()
        
        # Keep track of detection threads
        self.threads = []
        
        # Optional callback for external handling of recognized keywords
        self.callback = None
        
        # Lock to ensure only one thread calls the AI at a time
        self.ai_call_lock = threading.Lock()

    def load_model(self):
        print(f"Loading Vosk model from {self.model_path}...")
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Vosk model not found at {self.model_path}. Please ensure it is correctly unzipped.")
        model = Model(self.model_path)
        print("Model loaded successfully.")
        return model

    def keyword_detection_loop(self, thread_id, delay=0):
        if delay > 0:
            print(f"Thread {thread_id}: Delaying start by {delay} seconds...")
            time.sleep(delay)

        print(f"Thread {thread_id}: Starting detection loop.")
        recognizer = KaldiRecognizer(self.model, self.sample_rate)  # Independent recognizer per thread

        while self.running.is_set():
            try:
                # If we are already "talking_with_chat", skip recording
                if variables and variables.talking_with_chat:
                    # Another thread is already interacting with AI; just wait a bit
                    print(f"Thread {thread_id}: Paused detection (talking with ChatGPT)...")
                    time.sleep(1)
                    continue
                
                print(f"Thread {thread_id}: Listening for keywords...")
                audio_data = sd.rec(int(self.audio_duration * self.sample_rate),
                                    samplerate=self.sample_rate,
                                    channels=1, 
                                    dtype='int16')
                sd.wait()

                audio_stream = BytesIO()
                with wave.open(audio_stream, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)  # 'int16' => 2 bytes
                    wf.setframerate(self.sample_rate)
                    wf.writeframes(audio_data.tobytes())

                audio_stream.seek(0)
                wf = wave.open(audio_stream, "rb")

                detected_keywords = set()

                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    if recognizer.AcceptWaveform(data):
                        result = recognizer.Result()
                        result_dict = eval(result)
                        result_text = result_dict.get("text", "").lower()

                        for keyword in self.keywords:
                            if keyword.lower() in result_text:
                                if keyword.lower() not in detected_keywords:
                                    detected_keywords.add(keyword.lower())

                                    # If user provided a callback, call it
                                    if self.callback:
                                        self.callback(keyword, thread_id)

                                    # -------------------------------
                                    # Acquire the AI call lock here
                                    # -------------------------------
                                    with self.ai_call_lock:
                                        # Double-check if we're still not talking,
                                        # in case another thread beat us to it.
                                        if not variables.talking_with_chat:
                                            variables.talking_with_chat = True
                                            print(f"Thread {thread_id}: Calling AI Assistant...")

                                            text_to_speech("Calling Bruce, the AI assistant.")
                                            call_ai_assistant("Hey Brewsystem", thread_id)

                                            # Optionally set talking_with_chat back to False once done
                                            # Or keep it True if you want to maintain a longer conversation
                                            variables.talking_with_chat = False
                                    
                                # Break after we handle the first recognized keyword 
                                break

                time.sleep(self.audio_duration)

            except Exception as e:
                print(f"Thread {thread_id}: Error in detection loop: {e}")

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
