import json
import time
from openai import OpenAI
from pathlib import Path
import pygame
import sounddevice as sd
import wave
import sys, os
try:
    import Common.variables as variables
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    from Common import variables
except:
    pass


def record_audio(filename, duration=6, sample_rate=44100):
    """
    Records audio and saves it as a .wav file.
    """
    print("Recording (GPT)...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()
    print("Recording complete (GPT).")

    with wave.open(filename, "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_data.tobytes())

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
                print("Please speak your query (6 seconds max):")
                audio_path = "user_input.wav"

                # Record the user's query
                record_audio(audio_path)
                user_input = speech_to_text(audio_path)

                if not user_input:
                    print("No input detected. Please try again.")
                    text_to_speech("No input detected. Please try again.")
                    continue

                print(f"You: {user_input}")

                # Break the loop if the user says "exit" or "quit"
                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    text_to_speech("Goodbye!")
                    variables.talking_with_chat = False
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


def main():
    while True:
        print("Please speak your query (5 seconds max):")
        audio_path = "user_input.wav"

        # Record the user's query
        record_audio(audio_path)
        user_input = speech_to_text(audio_path)

        if not user_input:
            print("No input detected. Please try again.")
            continue

        print(f"You: {user_input}")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye!")
            break

        # Send the user input to the assistant and get the response
        conversation = [
            {"role": "user", "content": user_input}
        ]
        response = assistant_ai(conversation)
        print(f"Assistant: {response}")

        # Play the assistant's response aloud
        text_to_speech(response)

        # Ensure playback is complete before proceeding
        print("Playback complete. Ready for the next query.")

if __name__ == "__main__":
    main()
