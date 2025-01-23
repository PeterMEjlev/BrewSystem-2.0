from ChatGPT_API.Vosk_STT import KeywordDetector
import time

def handle_keyword(keyword, thread_id):
    print(f"Detected keyword: {keyword} (thread {thread_id})")
    

def main():
    detector = KeywordDetector(
        model_path="vosk-model-small-en-us-0.15",
        keywords=["brew system", "bruce system", "brew", "system", "bruce"],
    )

    # Start two detection threads with delays
    detector.start_detection(callback=handle_keyword, threads=2, delays=[0, 0.5])

    try:
        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        detector.stop_detection()

if __name__ == "__main__":
    main()
