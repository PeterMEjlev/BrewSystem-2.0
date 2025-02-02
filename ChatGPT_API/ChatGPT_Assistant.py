import json, time, pygame, wave, sys, os
from openai import OpenAI
from pathlib import Path
import sounddevice as sd
import numpy as np
from dotenv import dotenv_values
from ChatGPT_API import assistant_functions

config = dotenv_values("api_info.env")
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]
os.environ["OPENAI_ASSISTANT_ID"] = config["OPENAI_ASSISTANT_ID"]

# Retrieve them again
api_key = os.getenv("OPENAI_API_KEY")
assistant_id = os.getenv("OPENAI_ASSISTANT_ID")

try:
    import Common.variables as variables
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Common import variables
except:
    pass

def record_audio(filename, sample_rate=44100, silence_threshold=500, silence_duration=1.5):
    """
    Records audio until it hears some speech, then continues until `silence_duration`
    seconds of trailing silence occur. Saves the .wav file and returns whether we ever
    actually heard speech at all.
    """
    print("Recording (GPT)...")
    duration_per_chunk = 0.5  # seconds per chunk
    chunk_samples = int(sample_rate * duration_per_chunk)

    # The number of "silent" chunks needed to conclude "we're done speaking"
    silence_chunks = int(silence_duration / duration_per_chunk)

    # The number of chunks we allow before deciding "the user isn't speaking at all"
    max_wait_seconds = 1.5 
    max_chunks_no_speech = int(max_wait_seconds / duration_per_chunk)

    silence_counter = 0
    audio_buffer = []
    speech_detected = False
    chunks_without_speech = 0

    try:
        while True:
            audio_chunk = sd.rec(chunk_samples, samplerate=sample_rate, 
                                 channels=1, dtype='int16')
            sd.wait()

            chunk_float = audio_chunk.astype(np.float32)
            rms = np.sqrt(np.mean(chunk_float**2))

            print(f"Chunk RMS: {rms} - Silence Threshold: {silence_threshold}")
            audio_buffer.append(audio_chunk)

            if rms >= silence_threshold:
                # We have speech
                speech_detected = True
                chunks_without_speech = 0      # reset
                silence_counter = 0
            else:
                if not speech_detected:
                    # We haven't heard anything yet, increment no-speech counter
                    chunks_without_speech += 1
                    # If we've been silent too long at the start, stop
                    if chunks_without_speech >= max_chunks_no_speech:
                        print("No speech detected at all. Stopping.")
                        break
                else:
                    # We already heard speech, now checking trailing silence
                    silence_counter += 1

            # If we've started speaking, and now there's enough trailing silence
            if speech_detected and silence_counter >= silence_chunks:
                print("Silence detected after speech. Stopping recording.")
                break

        # Combine chunks and save
        audio_data = np.concatenate(audio_buffer, axis=0)
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())

        print("Recording complete (GPT).")
        return speech_detected

    except Exception as e:
        print(f"Error during recording: {e}")
        return False

def speech_to_text(audio_file_path , thread_id = None):
    """
    Transcribes audio to text using OpenAI's Whisper API.
    Returns None if no valid speech is detected.
    """
    try:
        openai_client = OpenAI(api_key=api_key)

        # Open the audio file in binary mode
        with open(audio_file_path, "rb") as audio_file:
            response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # Debugging: Check what the response contains
        print(f"Thread {thread_id}: Transcription response: {response}")

        # Access the transcription text
        if hasattr(response, "text") and response.text.strip():
            return response.text.strip()  # Return clean transcription text
        else:
            print("No valid speech detected.")
            return None  # Explicitly return None if no speech is detected

    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        return None

def handle_tool_call(function_name, parameters):
    try:
        if function_name == "toggle_pot":
            pot = parameters.get("pot", "unknown pot")
            state = parameters.get("state", "unknown state")
            return assistant_functions.toggle_pot(pot, state)
        elif function_name == "set_pot_efficiency":
            pot = parameters.get("pot", "unknown pot")
            efficiency = parameters.get("efficiency", "unknown efficiency")
            return assistant_functions.set_pot_efficiency(pot, efficiency)
        elif function_name == "set_reg_temperature":
            pot = parameters.get("pot", "unknown pot")
            temperature = parameters.get("temperature", "unknown temperature")
            return assistant_functions.set_reg_temperature(pot, temperature)
        
        elif function_name == "toggle_pump":
            pump = parameters.get("pump", "unknown pump")
            state = parameters.get("state", "unknown state")
            return assistant_functions.toggle_pump(pump, state)
        elif function_name == "set_pump_efficiency":
            pump = parameters.get("pump", "unknown pump")
            efficiency = parameters.get("efficiency", "unknown efficiency")
            return assistant_functions.set_pump_efficiency(pump, efficiency)
        
        elif function_name == "end_conversation":
            variables.talking_with_chat = False
            print("Ending the conversation.")
            return "Conversation ended successfully."
        else:
            return f"Function '{function_name}' not implemented."
    except Exception as e:
        return f"Error in handling tool call '{function_name}': {e}"

def text_to_speech(input_text):
    """
    Converts text to speech and plays the audio.
    """
    start_time = time.time()  # Start timing
    try:
        openai_client = OpenAI(api_key=api_key)

        speech_file_path = Path(__file__).parent / "speech.mp3"

        # Remove the file if it already exists and isn't in use
        if speech_file_path.exists():
            try:
                pygame.mixer.quit()  # Ensure the file is not locked by pygame
                speech_file_path.unlink()
            except Exception as e:
                print(f"Error deleting existing file: {e}")
                return

        # Generate spoken audio from the input text
        response = openai_client.audio.speech.create(
            model="tts-1",
            voice="ash",
            input=input_text,
        )
        response.stream_to_file(speech_file_path)

        end_time = time.time()  # Stop timing as soon as the file is ready
        print(f"text_to_speech() processing time: {end_time - start_time:.2f} seconds.")

        # Initialize the mixer before playback
        pygame.mixer.init()
        pygame.mixer.music.load(str(speech_file_path))
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        # Quit the mixer after playback is complete
        pygame.mixer.quit()
    except Exception as e:
        print(f"Error in text_to_speech: {e}")

def assistant_ai(conversation):
    try:
        openai_client = OpenAI(api_key=api_key)

        thread = openai_client.beta.threads.create(messages=conversation)
        run = openai_client.beta.threads.runs.create(
            thread_id=thread.id, assistant_id=assistant_id
        )

        while run.status not in ["completed", "failed", "requires_action"]:
            time.sleep(1)
            run = openai_client.beta.threads.runs.retrieve(
                thread_id=thread.id, run_id=run.id
            )

        if run.status == "failed":
            raise ValueError(f"Run failed with error: {run.last_error}")

        if run.status == "requires_action":
            tool_outputs = []
            for tool_call in run.required_action.submit_tool_outputs.tool_calls:
                function_name = tool_call.function.name
                parameters = json.loads(tool_call.function.arguments)
                output = handle_tool_call(function_name, parameters)
                tool_outputs.append({"tool_call_id": tool_call.id, "output": output})

            run = openai_client.beta.threads.runs.submit_tool_outputs_and_poll(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        if run.status == "completed":
            messages = openai_client.beta.threads.messages.list(thread_id=thread.id)
            for message in messages:
                if message.role == "assistant":
                    for block in message.content:
                        if block.type == "text":
                            return block.text.value

        return "Assistant response not found."

    except Exception as e:
        print(f"Error: {e}")
        return "Error occurred during processing."

def call_ai_assistant(starter_text="Hey Brewsystem", thread_id=None):
    """
    Starts the AI Assistant with a starter text and enables interactive conversation using speech-to-text.
    Stops if no valid speech is detected.
    """
    print(f"Call AI Assistant: {starter_text}")
    try:
        # Enable conversation mode
        variables.talking_with_chat = True
        print(f"talking_with_chat = {variables.talking_with_chat}")
        
        # Initialize conversation with the starter text
        conversation = [{"role": "user", "content": starter_text}]
        print(f"You: {starter_text}")

        # Send the starter text to the assistant
        response = assistant_ai(conversation)
        print(f"Assistant: {response}")

        # Respond to the starter text with TTS
        text_to_speech(response)

        # Interactive conversation loop
        while variables.talking_with_chat:
            print("Please speak your query:")
            audio_path = "user_input.wav"

            # Record user’s query and check if they actually spoke
            speech_found = record_audio(audio_path)
            if not speech_found:
                print("No input detected. Ending conversation.")
                text_to_speech("No input detected - Goodbye.")
                variables.talking_with_chat = False
                break

            # Transcribe the user’s query once
            user_input = speech_to_text(audio_path, thread_id)
            if not user_input:
                print("No valid speech detected. Ending conversation.")
                text_to_speech("No valid speech detected - Goodbye.")
                variables.talking_with_chat = False
                break

            print(f"You: {user_input}")

            # (Optional) Check for exit commands here if you want:
            # if check_for_exit_commands(user_input):
            #     break

            # Add the user input to the conversation
            conversation.append({"role": "user", "content": user_input})

            # Send the conversation to the assistant
            response = assistant_ai(conversation)
            print(f"Assistant: {response}")

            # Play the assistant's response aloud
            text_to_speech(response)

            # Ensure playback is complete before proceeding
            print("Playback complete. Ready for the next query.")

    except Exception as e:
        print(f"Error in call_ai_assistant: {e}")


def check_for_exit_commands(user_input):
    if any(word in user_input.lower() for word in ["exit", "quit", "end", "stop", "terminate"]):
                print(f"Goodbye!")
                text_to_speech("Goodbye!")
                variables.talking_with_chat = False
                print(f"talking_with_chat = {variables.talking_with_chat}")
                return True
                
