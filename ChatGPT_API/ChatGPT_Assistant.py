import json, time, pygame, wave, sys, os
from openai import OpenAI
from pathlib import Path
import sounddevice as sd
import numpy as np

try:
    import Common.variables as variables
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Common import variables
except:
    pass


def record_audio(filename, sample_rate=44100, silence_threshold=100, silence_duration=3):
    """
    Records audio until silence is detected and saves it as a .wav file.
    
    Parameters:
    - filename: The output .wav file name.
    - sample_rate: The sample rate of the audio.
    - silence_threshold: The RMS threshold below which audio is considered silent.
    - silence_duration: The number of consecutive seconds of silence to stop recording.
    """
    print("Recording (GPT)...")
    duration_per_chunk = 0.5  # Record in small chunks (0.5 seconds each)
    chunk_samples = int(sample_rate * duration_per_chunk)
    silence_chunks = int(silence_duration / duration_per_chunk)
    silence_counter = 0

    audio_buffer = []  # To store audio data

    try:
        while True:
            # Record a small chunk of audio
            audio_chunk = sd.rec(chunk_samples, samplerate=sample_rate, channels=1, dtype='int16')
            sd.wait()

            # Check for invalid values
            if np.isnan(audio_chunk).any():
                print("NaN values detected in audio_chunk. Skipping this chunk.")
                continue

            # Append the chunk to the buffer
            audio_buffer.append(audio_chunk)

            # Calculate RMS (volume) of the chunk
            try:
                rms = np.sqrt(np.mean(audio_chunk**2))
            except Exception as e:
                print(f"Error calculating RMS: {e}")
                rms = 0.0  # Treat as silence for safety

            # Debugging information
            print(f"Chunk RMS: {rms}, min: {np.min(audio_chunk)}, max: {np.max(audio_chunk)}")

            if rms < silence_threshold:
                silence_counter += 1
            else:
                silence_counter = 0  # Reset the counter if we detect speech

            # Stop recording if enough silence is detected
            if silence_counter >= silence_chunks:
                print("Silence detected. Stopping recording.")
                break

        # Combine all chunks into a single array
        audio_data = np.concatenate(audio_buffer, axis=0)

        # Save the recorded audio to a .wav file
        with wave.open(filename, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_data.tobytes())

        print("Recording complete (GPT).")
    except Exception as e:
        print(f"Error during recording: {e}")

def speech_to_text(audio_file_path):
    """
    Transcribes audio to text using OpenAI's Whisper API.
    """
    try:
        key = "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"
        openai_client = OpenAI(api_key=key)

        # Open the audio file in binary mode
        with open(audio_file_path, "rb") as audio_file:
            response = openai_client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # Debugging: Check what the response contains
        print(f"Transcription response: {response}")

        # Access the transcription text
        if hasattr(response, "text"):  # Check if 'text' attribute exists
            return response.text
        else:
            raise ValueError("Unexpected response format from the transcription API.")

    except Exception as e:
        print(f"Error in speech_to_text: {e}")
        return None

def set_reg_temperature(pot, temperature):
    print(f"Setting {pot} to {temperature}°C.")
    if pot == 'BK':
        variables.temp_REG_BK = temperature
    elif pot == 'HLT':
        variables.temp_REG_HLT = temperature

    return f"Regulation temperature for {pot} set to {temperature}°C."

def toggle_pot(pot, state):
    print(f"Toggling {pot} to {state}.")
    return f"Successfully toggled {pot} to {state}."

def handle_tool_call(function_name, parameters):
    try:
        if function_name == "toggle_pot":
            pot = parameters.get("pot", "unknown pot")
            state = parameters.get("state", "unknown state")
            return toggle_pot(pot, state)
        elif function_name == "set_reg_temperature":
            pot = parameters.get("pot", "unknown pot")
            temperature = parameters.get("temperature", "unknown temperature")
            return set_reg_temperature(pot, temperature)
        else:
            return f"Function '{function_name}' not implemented."
    except Exception as e:
        return f"Error in handling tool call '{function_name}': {e}"

def text_to_speech(input_text):
    """
    Converts text to speech and plays the audio.
    """
    try:
        key = "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"
        openai_client = OpenAI(api_key=key)

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
            voice="alloy",
            input=input_text,
        )
        response.stream_to_file(speech_file_path)

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
        assistant_id = "asst_fUBNWZV1aaTJWZH8yKCf1lnv"
        key = "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"
        openai_client = OpenAI(api_key=key)

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

def call_ai_assistant(starter_text="Hey Brewsystem"):
    """
    Starts the AI Assistant with a starter text and enables interactive conversation using speech-to-text.
    """
    print(f"Call AI Assistant: {starter_text}")
    if variables.talking_with_chat == False:
        try:
            variables.talking_with_chat = True
            # Initialize conversation with the starter text
            conversation = [{"role": "user", "content": starter_text}]
            print(f"You: {starter_text}")

            # Send the starter text to the assistant
            response = assistant_ai(conversation)
            print(f"Assistant: {response}")

            # Respond to the starter text with TTS
            text_to_speech(response)

            # Interactive conversation loop
            while True:
                print("Please speak your query:")
                audio_path = "user_input.wav"

                # Record the user's query
                record_audio(audio_path)
                user_input = speech_to_text(audio_path)

                if not user_input:
                    print("No input detected. Please try again.")
                    text_to_speech("No input detected. Please try again.")
                    continue

                print(f"DEBUG: user_input type = {type(user_input)}, value = {user_input}")
                print(f"You: {user_input}")
                if any(word in user_input.lower() for word in ["exit", "quit", "end", "stop", "terminate"]):
                    print("Goodbye!")
                    break

                # Add user input to the conversation
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

